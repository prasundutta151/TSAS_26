# ATNF Comparison

ATNF Pulsar Catalogue v2.8.1 was queried on 2026-06-24 for the 13 pulsars in `csv/sample_pulsar.csv` using `P0`, `W50`, `S1400`, `DM`, `PX`, `DIST`, `PMTOT`, and `VTRANS`.

The prompt-image table values are kept as table values. Current catalogue values are added where useful, with the two transverse-velocity columns placed side by side:

- `Vtrans table km/s`: value from the prompt image table
- `Vtrans catalog km/s`: current `VTRANS` value from ATNF v2.8.1

The two velocity columns differ because they come from different sources. The prompt image appears to be an older compiled table and does not include a citation in the screenshot. The catalogue column is from the current ATNF query, where `VTRANS` is derived from the catalogue distance and proper motion. If the original table source is available, cite it separately from ATNF.

For a fully catalogue-aligned sample, use `csv/sample_pulsar_ATNF.csv`. It uses ATNF values for the catalogue columns, recomputes `SW50` from ATNF `S1400`, `P0`, and `W50`, carries over `RMS`, `t5sigma`, and `Ton`, and removes `D (21) AU` and `D (22) AU`.

## Catalogue-Overlapping Columns

ATNF has direct matches for `P0`, `W50`, `S1400`, `DM`, and `VTRANS`. The sample table also has `SW50`, `RMS`, `t5sigma`, `Ton`, `D (21) AU`, and `D (22) AU`; those are not direct ATNF catalogue fields in this check.

`W50` is in milliseconds in both the prompt-image sample table and ATNF query output.

`P0` differs only by rounding in the prompt table. `DM` matches ATNF values after rounding. The main differences are in `W50`, `S1400`, and transverse velocity.

| Pulsar | Differences from ATNF v2.8.1 |
| --- | --- |
| B0329+54 | `Vtrans`: table 98.2, catalogue 158.401 km/s |
| B0736-40 | `W50`: table 29.0, catalogue 25.0 ms; `S1400`: table 80.0, catalogue 112.6 mJy; `Vtrans`: table 999.0, catalogue 361.330 km/s |
| B0950+08 | `W50`: table 9.5, catalogue 8.6 ms; `S1400`: table 84.0, catalogue 100.0 mJy |
| B1133+16 | `W50`: table 31.7, catalogue 5.8 ms; `S1400`: table 32.0, catalogue 20.0 mJy; `Vtrans`: table 635.7, catalogue 655.930 km/s |
| B1556-44 | `W50`: table 6.0, catalogue 6.3 ms; `S1400`: table 40.0, catalogue 37.0 mJy; `Vtrans`: table 163.4, catalogue 144.345 km/s |
| B1641-45 | `W50`: table 8.2, catalogue 8.0 ms; `S1400`: table 310.0, catalogue 300.0 mJy |
| B1642-03 | `W50`: table 4.2, catalogue 3.8 ms; `S1400`: table 21.0, catalogue 25.76 mJy; `Vtrans`: table 417.0, catalogue 389.250 km/s |
| B1713-40 | `W50`: table 15.0, catalogue 9.6 ms; `S1400`: table 54.0, catalogue 1.1 mJy |
| B1929+10 | `W50`: table 7.4, catalogue 5.6 ms; `S1400`: table 36.0, catalogue 29.0 mJy; `Vtrans`: table 177.1, catalogue 152.034 km/s |
| B1933+16 | `W50`: table 9.0, catalogue 6.5 ms; `S1400`: table 42.0, catalogue 58.0 mJy; `Vtrans`: table 347.6, catalogue 282.939 km/s |
| B2016+28 | `W50`: table 14.9, catalogue 15.5 ms; `Vtrans`: table 30.9, catalogue 31.236 km/s |
| B2020+28 | `W50`: table 12.0, catalogue 10.4 ms; `Vtrans`: table 307.6, catalogue 239.011 km/s |
| B2021+51 | `W50`: table 7.4, catalogue 11.9 ms; `Vtrans`: table 119.8, catalogue 107.810 km/s |

## Percentage Check

The script computes `delay/P0 (%)` as:

```text
(delay_ms / P0_ms) * 100
```

For example, with the included `rundir/run_example.sh`, B0329+54 has `delay = 7.75487e-05 ms` and `P0 = 0.715 s = 715 ms`, so:

```text
7.75487e-05 / 715 * 100 = 1.0846e-05 %
```
