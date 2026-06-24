# Requirements

TSAS is intentionally small. The pulsar-delay CLI uses only the Python standard library. The HI4PI fetch and plotting utilities use `requests` and `matplotlib`.

## Required

- Python 3.9 or newer
- `requests`
- `matplotlib`

Check your Python version:

```bash
python3 --version
```

On macOS, install Python with Homebrew if `python3` is not available:

```bash
brew install python
python3 -m pip install requests matplotlib
```

On Debian or Ubuntu:

```bash
sudo apt update
sudo apt install python3
python3 -m pip install requests matplotlib
```

## Run Without Installing

From the repository's `rundir/` directory:

```bash
cd rundir
./run_old_table.sh
./run_atnf_table.sh
```

Or run the CLI directly:

```bash
cd rundir
python3 ../script/pulsar_delay.py --input sample_pulsar.csv --reference-mhz 1420 --bandwidth-mhz 1
```

## Optional Package Install

For a local editable install that provides the `pulsar-delay` command:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -e .
```

Then run:

```bash
cd rundir
pulsar-delay --input sample_pulsar.csv --reference-mhz 1420 --bandwidth-mhz 1
pulsar-delay-old-table --reference-mhz 1420 --bandwidth-mhz 1
pulsar-delay-atnf-table --reference-mhz 1420 --bandwidth-mhz 1
```

## Optional Development Tools

These are useful for maintaining and publishing the project, but they are not needed to run the CLI:

- `git`, for version control
- `tar`, for rebuilding `dist/TSAS-0.1.0.tar.gz`
- GitHub SSH access or GitHub CLI, for pushing to GitHub

Install common tools on macOS:

```bash
xcode-select --install
brew install git
```

Install common tools on Debian or Ubuntu:

```bash
sudo apt update
sudo apt install git tar
```

## Rebuild The Distribution Tarball

From the repository root:

```bash
rm -f dist/TSAS-0.1.0.tar.gz
tar --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*/__pycache__' \
  --exclude='csv/*_with_delay.csv' \
  --exclude='csv/*_delay.csv' \
  --exclude='dist/TSAS-0.1.0.tar.gz' \
  -czf dist/TSAS-0.1.0.tar.gz .
```
