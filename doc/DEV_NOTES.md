# DEV_NOTES

## 24:6:26::12:08 Intent

Change output formatting so the delay is reported in nanoseconds to two decimal places, delay percentages are rounded to one decimal place, and `D(3mths) AU`/`D(6mths) AU` are rounded to one decimal place.

## 24:6:26::12:08 What Is Done

- Renamed the derived delay column from `delay (ms)` to `delay (ns)`.
- Converted delay output from milliseconds to nanoseconds.
- Added fixed-place output formatting for derived columns.
- Updated README Markdown/HTML and `doc/ATNF_COMPARISON.md`.
- Rebuilt `dist/TSAS-0.1.0.tar.gz`.

## 24:6:26::12:03 Intent

Add end-of-output travel-distance calculations giving how far each pulsar moves in 3 and 6 months in astronomical units, based on a transverse velocity column in km/s.

## 24:6:26::12:03 What Is Done

- Added `D(3mths) AU` and `D(6mths) AU` output columns at the end of generated CSVs.
- Added optional transverse-velocity column detection, preferring `V_trans km/s`, `Vtrans catalog km/s`, and related names.
- Used 0.25 and 0.5 Julian years for 3 and 6 months, with `1 AU = 149597870.7 km`.
- Updated README Markdown and HTML.
- Rebuilt `dist/TSAS-0.1.0.tar.gz`.

## 24:6:26::12:00 Intent

Correct the ATNF alternate CSV so its distance column is VLBI/parallax-only rather than ATNF's mixed-source best-estimate `DIST`. Blank distances when no `PX mas` value is listed, and recompute transverse velocities from ATNF proper motion and parallax-only distance for consistency.

## 24:6:26::12:00 What Is Done

- Updated `csv/sample_pulsar_ATNF.csv` so `DIST kpc = 1 / PX mas`.
- Left `DIST kpc` and `V_trans km/s` blank where `PX mas` is unavailable.
- Recomputed `V_trans km/s` using `4.74047 * PMTOT * DIST`.
- Updated README Markdown/HTML and `doc/ATNF_COMPARISON.md` to distinguish ATNF `DIST` from parallax-only distance.
- Rebuilt `dist/TSAS-0.1.0.tar.gz`.

## 24:6:26::11:55 Intent

Provide the reference for the dispersion-delay formula and correct the MHz-to-millisecond constant used by the script. The cited Lorimer & Kramer convention gives `4.148808 ms GHz^2 pc^-1 cm^3`; since the CLI accepts MHz and outputs milliseconds, the script should use `4.148808e6`.

## 24:6:26::11:55 What Is Done

- Updated the script dispersion constant from `4.148808e3` to `4.148808e6` for MHz inputs and millisecond outputs.
- Updated README Markdown and HTML formula text.
- Added the Lorimer & Kramer reference note to the README files.
- Updated the percentage-check example in `doc/ATNF_COMPARISON.md`.
- Rebuilt `dist/TSAS-0.1.0.tar.gz`.

## 24:6:26::11:47 Intent

Add an alternate ATNF-focused sample CSV that uses ATNF v2.8.1 values for `P0`, `W50`, `S1400`, `V_trans`, `DM`, `PX mas`, and `DIST kpc`, carries over `RMS`, `t5sigma`, and `Ton` from the existing sample, recomputes `SW50` from the ATNF quantities, and removes `D (21) AU` and `D (22) AU`.

## 24:6:26::11:47 What Is Done

- Added `csv/sample_pulsar_ATNF.csv`.
- Recomputed `SW50 mJy` as `S1400 mJy * P0_ms / W50_ms`.
- Left missing ATNF `PX` and `V_trans` values blank.
- Updated README Markdown/HTML and `doc/ATNF_COMPARISON.md`.
- Rebuilt `dist/TSAS-0.1.0.tar.gz`.

## 24:6:26::11:37 Intent

Add an explicit documentation note that `W50` is given in milliseconds, so `delay/W50 (%)` compares the computed delay in milliseconds with a millisecond pulse-width value.

## 24:6:26::11:37 What Is Done

- Updated README Markdown and HTML to state that `W50` is expected in milliseconds.
- Updated `doc/ATNF_COMPARISON.md` to state that both the sample table and ATNF query output use milliseconds for `W50`.
- Rebuilt `dist/TSAS-0.1.0.tar.gz`.

## 24:6:26::11:33 Intent

Verify whether `delay/P0 (%)` is multiplied by 100, rename the derived output columns to the requested presentation form, place old-table and current-catalog transverse velocities side by side, and document differences between prompt-image values and ATNF v2.8.1 where the catalogue has matching parameters.

## 24:6:26::11:33 What Is Done

- Confirmed `delay/P0 (%)` is computed as `(delay_ms / P0_ms) * 100`.
- Renamed derived output columns to `delay (ms)`, `delay/P0 (%)`, and `delay/W50 (%)`.
- Renamed/reordered velocity fields in `csv/sample_pulsar.csv` as `Vtrans table km/s` and `Vtrans catalog km/s`.
- Added `doc/ATNF_COMPARISON.md` with source clarification and parameter differences.
- Updated README Markdown and HTML.
- Rebuilt `dist/TSAS-0.1.0.tar.gz`.

## 24:6:26::11:22 Intent

Make the output CSV behavior explicit: preserve all original pulsar-table columns and append only the three requested derived columns for time delay, delay divided by `P0` as a percentage, and delay divided by `W50` as a percentage.

## 24:6:26::11:22 What Is Done

- Kept all input columns in their original order in the output CSV.
- Renamed the derived columns to `time_delay_ms`, `delay_over_P0_percent`, and `delay_over_W50_percent`.
- Updated README Markdown and HTML to document the preserved columns and derived output names.
- Rebuilt `dist/TSAS-0.1.0.tar.gz`.

## 24:6:26::11:19 Intent

Extend `csv/sample_pulsar.csv` with the ATNF v2.8.1 parallax/distance/proper-motion/velocity table previously checked for the same 13 pulsars. Treat `PX` as the ATNF parallax-based distance check for VLBI-style distance availability, preserve blank fields where ATNF reported `*`, rebuild the distribution tarball, and push the update.

## 24:6:26::11:19 What Is Done

- Added `PX mas`, `DIST kpc`, `PMTOT mas/yr`, and `VTRANS ATNF km/s` columns to `csv/sample_pulsar.csv`.
- Filled values for all 13 pulsars where ATNF v2.8.1 reports them.
- Left missing ATNF `*` values blank in the CSV.
- Rebuilt `dist/TSAS-0.1.0.tar.gz`.

## 24:6:26::11:17 Intent

Add a requirements document under `doc/` that explains what TSAS needs, how to get Python and optional development tools, how to run the CLI without installation, how to install the package locally, and how to rebuild the distribution tarball.

## 24:6:26::11:17 What Is Done

- Added `doc/REQUIREMENTS.md`.
- Documented that the CLI has no runtime third-party Python dependencies.
- Added Python, optional development-tool, editable-install, example-runner, and tarball rebuild instructions.
- Linked the requirements document from the README files.

## 24:6:26::11:18 Intent

Replace the short sample CSV with a complete `sample_pulsar.csv` based on the full pulsar list shown in the prompt image. Preserve the image-derived table columns, add dispersion measures for every listed pulsar, update the example runner and documentation, rebuild the distribution tarball, and push the refreshed repository.

## 24:6:26::11:18 What Is Done

- Renamed `csv/sample_pulsars.csv` to `csv/sample_pulsar.csv`.
- Added all 13 pulsars visible in the prompt image.
- Added DM values queried from ATNF Pulsar Catalogue v2.8.1.
- Updated `rundir/run_example.sh` to use `sample_pulsar.csv`.
- Updated documentation to describe the sample data source.
- Rebuilt the distribution tarball.

## 24:6:26::11:04 Intent

Reorganize the TSAS project so executable code lives under `script/`, user-facing documents live under `doc/`, and a small runnable example lives under `rundir/`. Refresh paths, rebuild the distribution tarball, recommit, and push the revised repository to `prasundutta151/TSAS_26`.

## 24:6:26::11:04 What Is Done

- Moved the Python CLI into `script/pulsar_delay.py`.
- Made `script/` importable for the package console entry point.
- Moved README Markdown, README HTML, and DEV_NOTES into `doc/`.
- Added `rundir/run_example.sh` to demonstrate the expected `../csv` input convention.
- Updated package metadata and documentation paths.
- Rebuilt `dist/TSAS-0.1.0.tar.gz`.

## 24:6:26::10:59 Intent

Build a small Python command-line utility for pulsar timing tables. The utility should read a CSV table from the neighboring `csv` directory, identify pulsar period, W50, and dispersion-measure columns, accept a reference frequency and bandwidth in MHz, and append the dispersive time delay across the band together with that delay as a percentage of the pulsar period and W50. If no output path is supplied, it should write beside the input using a `_with_delay` suffix.

## 24:6:26::10:59 What Is Done

- Created `pulsar_delay.py` with an `argparse` CLI and a `main()` entry point.
- Added flexible header matching for common `P0`, `W50`, and `DM` column names.
- Implemented the cold-plasma dispersion-delay calculation using the supplied reference frequency as the band center.
- Added README documentation in Markdown and HTML.
- Added version information in `VERSION`.
- Added a distributable tar archive under `dist/`.
