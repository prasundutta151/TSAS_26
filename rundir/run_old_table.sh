#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 ../script/pulsar_delay_old_table.py \
  --output sample_pulsar_delay.csv \
  --reference-mhz 1420.0 \
  --bandwidth-mhz 1.0
