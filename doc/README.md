# TSAS

TSAS adds dispersion-delay columns to pulsar CSV tables.

The CLI lives in `script/`. It reads a CSV from `../csv` relative to the directory where you run the command when a plain filename is supplied, calculates the dispersive time delay across an observing bandwidth, and writes a new CSV in the same directory unless `--output` is given.

The repository includes a `rundir/` folder with a small example script. Running from `rundir/` makes `../csv` point to the repository's sample CSV directory.

The included `csv/sample_pulsar.csv` file contains the full pulsar list from the prompt image, with dispersion measures added from the ATNF Pulsar Catalogue v2.8.1.

## Formula

The reference frequency is treated as the center of the band:

```text
low_mhz = reference_mhz - bandwidth_mhz / 2
high_mhz = reference_mhz + bandwidth_mhz / 2
delay_ms = 4.148808e3 * DM * (low_mhz^-2 - high_mhz^-2)
```

The script then reports:

- `delay_ms`
- `delay_period_percent`
- `delay_w50_percent`

## Required Columns

The input CSV needs columns for:

- pulsar period, such as `P0`, `P0 secs`, `period`, or `period_ms`
- W50 pulse width, such as `W50` or `W50 ms`
- dispersion measure, such as `DM` or `dispersion measure`

Missing numeric values represented by `?`, `-`, `--`, or a blank cell produce blank delay outputs for that row.

## Usage

Install and tool notes are in `doc/REQUIREMENTS.md`.

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
