# Results archive

The 40 deposited CSVs contain per-dataset mean scores for four benchmark
comparisons and supply the [league tables](../docs/league-tables/README.md).
Source files are preserved as supplied.

| Directory | Datasets | Estimators | Files | Primary measure |
| --- | --- | --- | --- | --- |
| [UCR](UCR/) | 112 | 10 | 11 | Accuracy |
| [Multiverse](multiverse/) | 60 | 12 | 11 | Accuracy |
| [TSER](TSER/) | 58 | 8 | 9 | RMSE |
| [Forecasting](TSFR/) | 100 | 12 | 9 | MSE |

The first CSV column (headed `Estimators:`) contains dataset IDs; subsequent
headers name estimators. All metric files within each collection have matching
rows and columns. [Dataset lists](../configs/datasets/README.md) are extracted
from these IDs. [manifest.json](manifest.json) records membership and SHA-256
checksums for every source CSV, plus negative-value and zero-value counts.
Negative R-squared values are valid; negative resource measurements indicate
unavailable data.

The manuscript specifies 30 resamples for UCR/TSER, the original partition for
Multiverse, and 30 rolling origins for forecasting. Mean files cannot verify
these counts. Raw predictions, per-resample/origin records and historical
software commits are not included. Ablation and simulation CSVs are absent;
those displayed tables remain manuscript snapshots.

## Measurements and availability

- UCR fit time and memory are `-1` for CIF, DrCIF, RISE, STSF and TSF. Their
  cells are marked unavailable, without substituting draft numbers.
- Timing is interpreted as milliseconds and memory as bytes from tsml-eval
  conventions and agreement with the manuscript scale. Mean CSVs have no unit
  metadata, so original run headers are needed to confirm this interpretation.
  Tables use seconds and MiB consistently; draft memory conversions varied
  across collections.
- Multivariate GPU timings remain in the CSVs but are omitted from the CPU
  comparison, following the paper.
- Forecasting contains MAPE but no sMAPE. sMAPE cannot be recovered from these
  means. Its table shows MSE, MAE and RMSE ranks. Many resource values are zero,
  so they are not used for a runtime comparison.
- `fitandestimatetime_mean.csv` contains unavailable values and is not used as
  a replacement for missing fit time.

## Regenerate

From an installed checkout, run `python tools/generate_results.py` to validate
coverage and rebuild the README, four benchmark pages, dataset lists and
checksum manifest. `interval-league` handles individual metrics and optional
pairwise tests; see [reproduction instructions](../docs/reproducing.md).

CSVs here are included in Git and excluded from Python distributions. New
experiment outputs default to ignored `local/`.
