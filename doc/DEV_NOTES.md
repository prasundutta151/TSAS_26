# DEV_NOTES

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
