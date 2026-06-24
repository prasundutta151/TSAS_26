#!/usr/bin/env python3
"""Compute dispersion-delay fractions for a pulsar CSV table."""

from __future__ import annotations

import argparse
import csv
import math
import re
from pathlib import Path
from typing import Iterable


VERSION = "0.1.0"
DISPERSION_CONSTANT_MS = 4.148808e6
DEFAULT_CSV_DIR = Path.cwd() / ".." / "csv"
JULIAN_YEAR_SECONDS = 365.25 * 24.0 * 60.0 * 60.0
AU_KM = 149_597_870.7
OUTPUT_DELAY_COLUMN = "delay (ns)"
OUTPUT_P0_PERCENT_COLUMN = "delay/P0 (%)"
OUTPUT_W50_PERCENT_COLUMN = "delay/W50 (%)"
OUTPUT_D_3_MONTHS_COLUMN = "D(3mths) AU"
OUTPUT_D_6_MONTHS_COLUMN = "D(6mths) AU"


class ColumnLookupError(ValueError):
    """Raised when a required input column cannot be identified."""


def normalize_header(name: str) -> str:
    """Return a relaxed header key for matching science-table labels."""
    return re.sub(r"[^a-z0-9]+", "", name.casefold())


def find_column(headers: Iterable[str], aliases: Iterable[str]) -> str:
    normalized = {normalize_header(header): header for header in headers}
    for alias in aliases:
        key = normalize_header(alias)
        if key in normalized:
            return normalized[key]
    raise ColumnLookupError(
        "Could not find any of these columns: " + ", ".join(sorted(aliases))
    )


def find_optional_column(headers: Iterable[str], aliases: Iterable[str]) -> str | None:
    normalized = {normalize_header(header): header for header in headers}
    for alias in aliases:
        key = normalize_header(alias)
        if key in normalized:
            return normalized[key]
    return None


def parse_float(value: str, column: str, row_number: int) -> float:
    text = strip_marker(value)
    if not text or text in {"?", "-", "--", "nan", "NaN"}:
        return math.nan
    try:
        return float(text)
    except ValueError as exc:
        raise ValueError(
            f"Row {row_number}: column {column!r} contains non-numeric value {value!r}"
        ) from exc


def strip_marker(value: str) -> str:
    return (value or "").strip().rstrip("*").strip()


def has_marker(value: str) -> bool:
    return (value or "").strip().endswith("*")


def period_to_ms(period_value: float, period_column: str) -> float:
    column_key = normalize_header(period_column)
    if "ms" in column_key or "millisecond" in column_key:
        return period_value
    return period_value * 1000.0


def delay_across_band_ms(dm: float, reference_mhz: float, bandwidth_mhz: float) -> float:
    low_mhz = reference_mhz - (bandwidth_mhz / 2.0)
    high_mhz = reference_mhz + (bandwidth_mhz / 2.0)
    if low_mhz <= 0:
        raise ValueError(
            "Reference frequency minus half the bandwidth must be greater than 0 MHz"
        )
    return DISPERSION_CONSTANT_MS * dm * ((low_mhz**-2) - (high_mhz**-2))


def transverse_distance_au(velocity_km_s: float, year_fraction: float) -> float:
    return velocity_km_s * JULIAN_YEAR_SECONDS * year_fraction / AU_KM


def resolve_input_path(input_value: str) -> Path:
    candidate = Path(input_value).expanduser()
    if candidate.is_absolute():
        return candidate

    if candidate.parent == Path("."):
        csv_candidate = (DEFAULT_CSV_DIR / candidate).resolve()
        if csv_candidate.exists():
            return csv_candidate

    if candidate.exists():
        return candidate

    return candidate.resolve()


def resolve_output_path(output_value: str | None, input_path: Path) -> Path:
    if output_value:
        candidate = Path(output_value).expanduser()
        if candidate.is_absolute() or candidate.parent != Path("."):
            return candidate.resolve()
        return (input_path.parent / candidate).resolve()

    return input_path.with_name(f"{input_path.stem}_with_delay{input_path.suffix}")


def process_csv(input_path: Path, output_path: Path, reference_mhz: float, bandwidth_mhz: float) -> None:
    if reference_mhz <= 0:
        raise ValueError("Reference frequency must be greater than 0 MHz")
    if bandwidth_mhz <= 0:
        raise ValueError("Bandwidth must be greater than 0 MHz")
    if reference_mhz - (bandwidth_mhz / 2.0) <= 0:
        raise ValueError("Bandwidth is too large for the supplied reference frequency")

    with input_path.open("r", newline="", encoding="utf-8-sig") as input_file:
        reader = csv.DictReader(input_file)
        if not reader.fieldnames:
            raise ValueError(f"{input_path} does not contain a CSV header row")

        headers = list(reader.fieldnames)
        period_column = find_column(
            headers,
            {
                "P0",
                "P_0",
                "P0 secs",
                "P0 seconds",
                "period",
                "period seconds",
                "period_ms",
            },
        )
        w50_column = find_column(
            headers,
            {"W50", "W_50", "W50 ms", "pulse width w50", "width50", "width_50"},
        )
        dm_column = find_column(
            headers,
            {
                "DM",
                "dispersion measure",
                "dispersion_measure",
                "dispersion measure pc cm-3",
                "dm pc cm-3",
            },
        )
        velocity_column = find_optional_column(
            headers,
            [
                "V_trans km/s",
                "Vtrans catalog km/s",
                "VTRANS ATNF km/s",
                "Vtrans km/s",
                "Vtrans table km/s",
                "Vtrans",
            ],
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_fields = headers + [
            OUTPUT_DELAY_COLUMN,
            OUTPUT_P0_PERCENT_COLUMN,
            OUTPUT_W50_PERCENT_COLUMN,
            OUTPUT_D_3_MONTHS_COLUMN,
            OUTPUT_D_6_MONTHS_COLUMN,
        ]

        with output_path.open("w", newline="", encoding="utf-8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=output_fields)
            writer.writeheader()

            for row_number, row in enumerate(reader, start=2):
                dm = parse_float(row.get(dm_column, ""), dm_column, row_number)
                period = parse_float(row.get(period_column, ""), period_column, row_number)
                w50_ms = parse_float(row.get(w50_column, ""), w50_column, row_number)
                if velocity_column:
                    velocity_has_marker = has_marker(row.get(velocity_column, ""))
                    velocity_km_s = parse_float(
                        row.get(velocity_column, ""), velocity_column, row_number
                    )
                else:
                    velocity_has_marker = False
                    velocity_km_s = math.nan

                if math.isnan(dm) or math.isnan(period) or math.isnan(w50_ms):
                    delay_ms = math.nan
                    period_percent = math.nan
                    w50_percent = math.nan
                else:
                    period_ms = period_to_ms(period, period_column)
                    delay_ms = delay_across_band_ms(dm, reference_mhz, bandwidth_mhz)
                    period_percent = (delay_ms / period_ms) * 100.0
                    w50_percent = (delay_ms / w50_ms) * 100.0

                if math.isnan(velocity_km_s):
                    distance_3_months = math.nan
                    distance_6_months = math.nan
                else:
                    distance_3_months = transverse_distance_au(velocity_km_s, 0.25)
                    distance_6_months = transverse_distance_au(velocity_km_s, 0.5)

                row[OUTPUT_DELAY_COLUMN] = format_fixed(delay_ms * 1_000_000.0, 2)
                row[OUTPUT_P0_PERCENT_COLUMN] = format_fixed(period_percent, 1)
                row[OUTPUT_W50_PERCENT_COLUMN] = format_fixed(w50_percent, 1)
                row[OUTPUT_D_3_MONTHS_COLUMN] = format_fixed(
                    distance_3_months, 1, marker=velocity_has_marker
                )
                row[OUTPUT_D_6_MONTHS_COLUMN] = format_fixed(
                    distance_6_months, 1, marker=velocity_has_marker
                )
                writer.writerow(row)


def format_fixed(value: float, places: int, marker: bool = False) -> str:
    if math.isnan(value):
        return ""
    suffix = "*" if marker else ""
    return f"{value:.{places}f}{suffix}"


def build_parser(default_input: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Add pulsar dispersion-delay percentages to a CSV table."
    )
    parser.add_argument(
        "--input",
        default=default_input,
        required=default_input is None,
        help="Input CSV path or filename in ../csv relative to the run directory.",
    )
    parser.add_argument(
        "--output",
        help="Output CSV path. Defaults to <input>_with_delay.csv in the input directory.",
    )
    parser.add_argument(
        "--reference-mhz",
        type=float,
        required=True,
        help="Reference frequency in MHz, interpreted as the band center.",
    )
    parser.add_argument(
        "--bandwidth-mhz",
        type=float,
        required=True,
        help="Observing bandwidth in MHz.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    return parser


def run_cli(argv: list[str] | None = None, default_input: str | None = None) -> int:
    parser = build_parser(default_input)
    args = parser.parse_args(argv)

    try:
        input_path = resolve_input_path(args.input)
        output_path = resolve_output_path(args.output, input_path)
        process_csv(input_path, output_path, args.reference_mhz, args.bandwidth_mhz)
    except (ColumnLookupError, OSError, ValueError) as exc:
        parser.exit(1, f"error: {exc}\n")

    print(f"Wrote {output_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    return run_cli(argv)


if __name__ == "__main__":
    raise SystemExit(main())
