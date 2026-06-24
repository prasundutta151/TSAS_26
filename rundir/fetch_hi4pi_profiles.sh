#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 ../script/fetch_hi4pi_profiles.py
