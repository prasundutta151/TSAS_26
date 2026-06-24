# TSAS

TSAS adds dispersion-delay columns to pulsar CSV tables.

The CLI code lives in `script/`. The shared calculation engine is `script/pulsar_delay.py`, with two table-specific entry points:

- `script/pulsar_delay_old_table.py` defaults to `csv/sample_pulsar.csv`
- `script/pulsar_delay_atnf_table.py` defaults to `csv/sample_pulsar_ATNF.csv`

Each entry point reads from `../csv` relative to the directory where you run the command, preserves all input columns, calculates the dispersive time delay across an observing bandwidth, and writes a new CSV in the same directory unless `--output` is given.

The repository includes a `rundir/` folder with two small runner scripts. Running from `rundir/` makes `../csv` point to the repository's sample CSV directory.

The included `csv/sample_pulsar.csv` file contains the full pulsar list from the prompt image, with dispersion measures added from the ATNF Pulsar Catalogue v2.8.1.

The alternate `csv/sample_pulsar_ATNF.csv` file uses ATNF v2.8.1 values for `P0`, `W50`, `S1400`, `V_trans`, `DM`, `PX mas`, and best `DIST kpc`. Distances and velocities marked with `*` are ATNF best estimates but are not VLBI/parallax distances. `SW50` is recomputed as `S1400 * P0_ms / W50_ms`, while `RMS`, `t5sigma`, and `Ton` are carried over from the prompt-image sample. The `D (21) AU` and `D (22) AU` columns are omitted from this ATNF-focused sample.

## Formula

The reference frequency is treated as the center of the band:

```text
low_mhz = reference_mhz - bandwidth_mhz / 2
high_mhz = reference_mhz + bandwidth_mhz / 2
delay_ms = 4.148808e6 * DM * (low_mhz^-2 - high_mhz^-2)
```

The script then reports:

- `delay (ns)`
- `delay/P0 (%)`
- `delay/W50 (%)`
- `D(3mths) AU`
- `D(6mths) AU`

The output delay is converted from milliseconds to nanoseconds and rounded to two decimal places. Delay percentages and travel distances are rounded to one decimal place.

`W50` is expected to be given in milliseconds. In the sample table this is the `W50 ms` column, so `delay/W50 (%)` compares two millisecond quantities directly.

The `D(3mths) AU` and `D(6mths) AU` columns use the transverse velocity in km/s, if present, to compute how far the pulsar travels across the sky in 0.25 and 0.5 Julian years. The calculation is `velocity_km_s * elapsed_seconds / 149597870.7`.

If the input transverse velocity has a trailing `*`, the script treats it as numeric but propagates the `*` to `D(3mths) AU` and `D(6mths) AU` to show that a non-parallax distance entered the quoted velocity.

## Required Columns

The input CSV needs columns for:

- pulsar period, such as `P0`, `P0 secs`, `period`, or `period_ms`
- W50 pulse width in milliseconds, such as `W50` or `W50 ms`
- dispersion measure, such as `DM` or `dispersion measure`

For the travel-distance columns, the script also uses a transverse-velocity column when present, preferring names such as `V_trans km/s`, `Vtrans catalog km/s`, or `Vtrans km/s`.

Missing numeric values represented by `?`, `-`, `--`, or a blank cell produce blank delay outputs for that row.

## Usage

Install and tool notes are in `doc/REQUIREMENTS.md`.

For the prompt-image/old-table sample:

```bash
cd rundir
./run_old_table.sh
```

For the ATNF/parallax-distance sample:

```bash
cd rundir
./run_atnf_table.sh
```

The generic CLI can still be used with any compatible CSV:

```bash
python3 ../script/pulsar_delay.py --input pulsars.csv --reference-mhz 1400 --bandwidth-mhz 100
```

With an explicit output filename:

```bash
python3 ../script/pulsar_delay.py --input pulsars.csv --output pulsars_delay.csv --reference-mhz 1400 --bandwidth-mhz 100
```

If the input is `../csv/pulsars.csv` and `--output` is omitted, the output is:

```text
../csv/pulsars_with_delay.csv
```

## Version

Current version: `0.1.0`

## Distribution

The distribution tarball is written to `dist/TSAS-0.1.0.tar.gz`.

## Data Note

The sample DM values are from the ATNF Pulsar Catalogue. ATNF requests acknowledgement of the catalogue web address and Manchester, Hobbs, Teoh & Hobbs, AJ, 129, 1993-2006 (2005), when catalogue data are used in publications.

The sample table keeps the prompt-image transverse velocity beside the current catalogue transverse velocity as `Vtrans table km/s` and `Vtrans catalog km/s`. A comparison against ATNF v2.8.1 is in `doc/ATNF_COMPARISON.md`.

The dispersion-delay constant follows Lorimer & Kramer, *Handbook of Pulsar Astronomy* (Cambridge University Press, 2005): `4.148808 ms GHz^2 pc^-1 cm^3`. With frequencies supplied in MHz, this becomes `4.148808e6 ms MHz^2 pc^-1 cm^3`.
