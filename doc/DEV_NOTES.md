# DEV_NOTES

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
