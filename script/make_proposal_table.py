#!/usr/bin/env python3
"""Create the proposal Table 1 from the ATNF pulsar CSV."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


N_ANTE = 26
DELTA_NU_HZ = 9600.0
T_ON_SEC = 3600.0
AU_KM = 1.495978707e8
THREE_MONTHS_SEC = 3 * 30 * 24 * 3600


CSV_COLUMNS = [
    "Pulsar",
    "DM pc cm^-3",
    "P0 s",
    "W50 ms",
    "S1400 mJy",
    "SW50 mJy",
    "TBmax K",
    "SRMS mJy",
    "tau_5sigma",
    "V_trans km/s",
    "D_3months AU",
]


def parse_float(value: str) -> float | None:
    value = value.strip().replace("*", "")
    if not value:
        return None
    return float(value)


def fmt(value: float | None, places: int) -> str:
    if value is None:
        return "--"
    return f"{value:.{places}f}"


def make_row(row: dict[str, str]) -> dict[str, str]:
    pulsar = row["Pulsar"]
    p0 = float(row["P0 secs"])
    w50_ms = float(row["W50 ms"])
    w50_sec = w50_ms / 1000.0
    s1400 = float(row["S1400 mJy"])
    dm = float(row["DM"])
    tbmax = float(row["HI peak T K"])
    vtrans = parse_float(row["V_trans km/s"])

    sw50 = s1400 * p0 / w50_sec
    denominator = math.sqrt(
        2 * N_ANTE * (N_ANTE + 1) * DELTA_NU_HZ * T_ON_SEC * w50_sec / p0
    )
    srms = ((70.0 + tbmax) / 0.22) / denominator * 1000.0
    tau_5sigma = 5.0 * srms / sw50
    d_3months = None if vtrans is None else vtrans * THREE_MONTHS_SEC / AU_KM

    return {
        "Pulsar": pulsar,
        "DM pc cm^-3": fmt(dm, 1),
        "P0 s": fmt(p0, 3),
        "W50 ms": fmt(w50_ms, 1),
        "S1400 mJy": fmt(s1400, 1),
        "SW50 mJy": fmt(sw50, 1),
        "TBmax K": fmt(tbmax, 1),
        "SRMS mJy": fmt(srms, 1),
        "tau_5sigma": fmt(tau_5sigma, 3),
        "V_trans km/s": fmt(vtrans, 1),
        "D_3months AU": fmt(d_3months, 1),
    }


def read_table(input_path: Path) -> list[dict[str, str]]:
    with input_path.open(newline="") as handle:
        return [make_row(row) for row in csv.DictReader(handle)]


def write_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def latex_escape(value: str) -> str:
    return value.replace("_", r"\_")


def write_latex(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        r"\begin{table}[t!]",
        r"\begin{center}",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}[h]{|c|c|c|c|c|c|c|c|c|c|c|}",
        r"\hline",
        (
            r"Pulsar & DM & $P_0$ & $W_{50}$ & $S_{1400}$ & $S_{W50}$ & "
            r"$T_{B{\rm max}}$ & $S_{\rm RMS}$ & $\tau_{5\sigma}$ & "
            r"$V_{\rm trans}$ & $D_{3{\rm months}}$ \\"
        ),
        (
            r"       & pc~cm$^{-3}$ & s & ms & mJy & mJy & K & mJy & "
            r"& km~s$^{-1}$ & AU \\"
        ),
        r"\hline",
    ]

    for row in rows:
        lines.append(
            " & ".join(latex_escape(row[column]) for column in CSV_COLUMNS) + r" \\"
        )

    lines.extend(
        [
            r"\hline",
            r"\end{tabular}",
            r"}",
            r"\caption{here goes the caption.}",
            r"\end{center}",
            r"\end{table}",
            "",
        ]
    )
    output_path.write_text("\n".join(lines))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create proposal Table 1 from the ATNF pulsar CSV."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="csv/sample_pulsar_ATNF.csv",
        help="Input ATNF CSV file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="csv/Table1.csv",
        help="Output CSV table path.",
    )
    parser.add_argument(
        "--latex",
        action="store_true",
        help="Also write the LaTeX table.",
    )
    parser.add_argument(
        "--latex-output",
        default="latex/Table1.tex",
        help="Output LaTeX table path used with --latex.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = read_table(Path(args.input))
    write_csv(rows, Path(args.output))
    if args.latex:
        write_latex(rows, Path(args.latex_output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
