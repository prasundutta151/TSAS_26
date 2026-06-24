#!/usr/bin/env python3
"""Plot all TSAS HI4PI profiles in three side-by-side panels."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


DEFAULT_CSV_DIR = Path.cwd() / ".." / "csv"
GROUPS = [
    ["B0329+54", "B0736-40", "B0950+08", "B1133+16", "B1556-44"],
    ["B1641-45", "B1642-03", "B1713-40", "B1929+10"],
    ["B1933+16", "B2016+28", "B2020+28", "B2021+51"],
]


def safe_name(name: str) -> str:
    return name.replace("+", "p").replace("-", "m")


def read_profile(path: Path) -> tuple[list[float], list[float]]:
    velocities: list[float] = []
    temperatures: list[float] = []
    with path.open("r", newline="", encoding="utf-8") as input_file:
        for row in csv.DictReader(input_file):
            velocities.append(float(row["velocity_lsr_km_s"]))
            temperatures.append(float(row["brightness_temperature_K"]))
    return velocities, temperatures


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plot TSAS HI4PI profiles in three panels.")
    parser.add_argument("--input-dir", default=str(DEFAULT_CSV_DIR), help="Directory containing HI4PI profile CSVs.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_CSV_DIR / "hi4pi_profiles_three_panel.png"),
        help="Output plot path.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    input_dir = Path(args.input_dir).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharex=True, sharey=True)
    for axis, group in zip(axes, GROUPS):
        for pulsar in group:
            path = input_dir / f"hi4pi_profile_{safe_name(pulsar)}.csv"
            velocities, temperatures = read_profile(path)
            axis.plot(velocities, temperatures, linewidth=1.2, label=pulsar)
        axis.axhline(0.0, color="0.6", linewidth=0.6)
        axis.set_title(", ".join(group), fontsize=9)
        axis.set_xlabel("LSR velocity (km/s)")
        axis.grid(alpha=0.25, linewidth=0.5)
        axis.legend(fontsize=8, loc="upper right")

    axes[0].set_ylabel("Brightness temperature (K)")
    fig.suptitle("HI4PI Gaussian 21-cm Profiles Toward TSAS Pulsars")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
