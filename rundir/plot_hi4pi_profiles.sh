#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 ../script/plot_hi4pi_profiles.py
