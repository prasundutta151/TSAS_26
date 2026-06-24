#!/usr/bin/env python3
"""Fetch HI4PI Gaussian 21-cm profiles for the TSAS pulsar sample."""

from __future__ import annotations

import argparse
import csv
import re
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlencode

import requests


BASE_URL = "https://www.astro.uni-bonn.de/hisurvey/AllSky_gauss/download.php"
DEFAULT_CSV_DIR = Path.cwd() / ".." / "csv"


@dataclass(frozen=True)
class PulsarPosition:
    name: str
    glon: float
    glat: float
    raj: str
    decj: str


PULSARS = [
    PulsarPosition("B0329+54", 144.995, -1.221, "03:32:59.4", "+54:34:43.3"),
    PulsarPosition("B0736-40", 254.193, -9.192, "07:38:32.3", "-40:42:40.1"),
    PulsarPosition("B0950+08", 228.908, 43.697, "09:53:09.3", "+07:55:35.7"),
    PulsarPosition("B1133+16", 241.895, 69.196, "11:36:03.1", "+15:51:14.1"),
    PulsarPosition("B1556-44", 334.540, 6.367, "15:59:41.5", "-44:38:45.9"),
    PulsarPosition("B1641-45", 339.193, -0.195, "16:44:49.2", "-45:59:09.7"),
    PulsarPosition("B1642-03", 14.114, 26.062, "16:45:02.0", "-03:17:57.8"),
    PulsarPosition("B1713-40", 346.759, -1.893, "17:17:52.3", "-41:03:17.8"),
    PulsarPosition("B1929+10", 47.382, -3.885, "19:32:14.0", "+10:59:33.3"),
    PulsarPosition("B1933+16", 52.436, -2.093, "19:35:47.8", "+16:16:39.9"),
    PulsarPosition("B2016+28", 68.099, -3.983, "20:18:03.8", "+28:39:54.2"),
    PulsarPosition("B2020+28", 68.863, -4.671, "20:22:37.0", "+28:54:23.1"),
    PulsarPosition("B2021+51", 87.862, 8.380, "20:22:49.8", "+51:54:50.2"),
]


def safe_name(name: str) -> str:
    return name.replace("+", "p").replace("-", "m")


def fetch_ascii_profile(
    pulsar: PulsarPosition,
    beam_deg: float,
    velocity_min: float,
    velocity_max: float,
    timeout_s: float,
) -> str:
    params = {
        "ral": f"{pulsar.glon:.3f}",
        "decb": f"{pulsar.glat:.3f}",
        "csys": "0",
        "beam": f"{beam_deg:.3f}",
        "vmin": f"{velocity_min:.2f}",
        "vmax": f"{velocity_max:.2f}",
    }
    url = f"{BASE_URL}?{urlencode(params)}"
    response = requests.get(url, timeout=timeout_s)
    response.raise_for_status()
    return response.text


def extract_gaussian_profile(ascii_text: str) -> list[tuple[float, float]]:
    rows: list[tuple[float, float]] = []
    in_gauss = False
    for line in ascii_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("%%gauss") and "datapoints" in stripped:
            in_gauss = True
            continue
        if in_gauss and stripped.startswith("%%"):
            break
        if not in_gauss or not stripped or stripped.startswith("%"):
            continue
        parts = stripped.split()
        if len(parts) < 2:
            continue
        rows.append((float(parts[0]), float(parts[1])))
    if not rows:
        raise ValueError("No HI4PI Gaussian profile rows found in download")
    return rows


def parse_column_density(ascii_text: str) -> str:
    match = re.search(r"%\s+[^;]+;\s+[^;]+;\s+[^;]+;\s+[^;]+;\s+([0-9.E+-]+)\s*;", ascii_text)
    return match.group(1) if match else ""


def write_profile_csv(path: Path, pulsar: PulsarPosition, rows: list[tuple[float, float]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["pulsar", "velocity_lsr_km_s", "brightness_temperature_K"])
        for velocity, tb in rows:
            writer.writerow([pulsar.name, f"{velocity:.2f}", f"{tb:.6g}"])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch HI4PI Gaussian profiles for TSAS pulsars.")
    parser.add_argument("--output-dir", default=str(DEFAULT_CSV_DIR), help="Directory for profile CSV files.")
    parser.add_argument("--beam-deg", type=float, default=0.2, help="Effective beam FWHM in degrees.")
    parser.add_argument("--velocity-min", type=float, default=-400.0, help="Minimum LSR velocity in km/s.")
    parser.add_argument("--velocity-max", type=float, default=400.0, help="Maximum LSR velocity in km/s.")
    parser.add_argument("--sleep-s", type=float, default=0.25, help="Pause between service requests.")
    parser.add_argument("--timeout-s", type=float, default=60.0, help="HTTP timeout in seconds.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    index_path = output_dir / "hi4pi_profile_index.csv"
    with index_path.open("w", newline="", encoding="utf-8") as index_file:
        index_writer = csv.writer(index_file)
        index_writer.writerow(
            [
                "pulsar",
                "profile_file",
                "glon_deg",
                "glat_deg",
                "raj",
                "decj",
                "beam_deg",
                "velocity_min_km_s",
                "velocity_max_km_s",
                "source",
                "nhi_cm-2",
            ]
        )

        for pulsar in PULSARS:
            ascii_text = fetch_ascii_profile(
                pulsar,
                beam_deg=args.beam_deg,
                velocity_min=args.velocity_min,
                velocity_max=args.velocity_max,
                timeout_s=args.timeout_s,
            )
            rows = extract_gaussian_profile(ascii_text)
            profile_name = f"hi4pi_profile_{safe_name(pulsar.name)}.csv"
            write_profile_csv(output_dir / profile_name, pulsar, rows)
            index_writer.writerow(
                [
                    pulsar.name,
                    profile_name,
                    f"{pulsar.glon:.3f}",
                    f"{pulsar.glat:.3f}",
                    pulsar.raj,
                    pulsar.decj,
                    f"{args.beam_deg:.3f}",
                    f"{args.velocity_min:.2f}",
                    f"{args.velocity_max:.2f}",
                    "Bonn AIfA HI Profile Search, HI4PI Gaussian profile",
                    parse_column_density(ascii_text),
                ]
            )
            print(f"Wrote {output_dir / profile_name}")
            time.sleep(args.sleep_s)

    print(f"Wrote {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
