#!/usr/bin/env python3
"""Run pulsar-delay calculations for the prompt-image sample table."""

from __future__ import annotations

try:
    from .pulsar_delay import run_cli
except ImportError:
    from pulsar_delay import run_cli


def main() -> int:
    return run_cli(default_input="sample_pulsar.csv")


if __name__ == "__main__":
    raise SystemExit(main())
