# Reproducing the study

Install the checkout with `python -m pip install -e ".[experiments,dev]"`.
Core estimators depend on [aeon](https://www.aeon-toolkit.org/) and
[tsml](https://github.com/time-series-machine-learning/tsml-py); archive execution
uses [tsml-eval](https://github.com/time-series-machine-learning/tsml-eval).
Acquire data separately using the archive's licensing and download instructions.
For multivariate data use the [Multiverse archive](https://github.com/aeon-toolkit/multiverse).

## Archive classification and regression

Place `.ts` files at `data/<dataset>/<dataset>_TRAIN.ts` and the corresponding
`_TEST.ts` path. Use explicit dataset names for a small run:

```bash
interval-benchmark --task ucr --data-path data --datasets GunPoint --estimators quant --resamples 0
interval-benchmark --task multivariate --data-path data --datasets BasicMotions --estimators pulsar --resamples 0
interval-benchmark --task tser --data-path data --datasets Covid3Month --estimators quant --resamples 0
```

For a full collection, supply a frozen newline-delimited list with
`--dataset-list configs/datasets/<name>.txt`. Blank lines and `#` comments are
ignored. `ucr112.txt`, `multiverse60.txt` and `tser58.txt` are extracted from
the deposited CSVs; `ucr103.txt` remains pending the ablation files.
`--dry-run` constructs and prints the plan.
UCR, TSER and ablation tasks default to resamples 0–29; multivariate permits only
resample 0. tsml-eval handles classification stratification and its regression
resampling procedure. All fitting and feature selection use training data.

```bash
interval-benchmark --task ablation --data-path data --dataset-list configs/datasets/ucr103.txt --estimators pulsar pulsar-et pulsar-ridge pulsar-nopool pulsar-nosel pulsar-noar quant drcif --dry-run
```

The list in that example must be supplied from the final runs before execution.
Existing prediction files are skipped. Every new run records package versions,
available installation origin metadata and constructor parameters in a JSON
sidecar; prediction files use the standard tsml-eval format. Default output is
`local/results/`, separate from the eventual published archive.

## Alignment simulations

```bash
interval-simulate --dry-run
interval-simulate --estimators quant --strengths 1 --placements aligned --replicates 1
interval-simulate --estimators pulsar pulsar-nopool pulsar-nosel pulsar-noar pulsar-et pulsar-ridge tsf rocket --strengths 1 --placements aligned uniform --replicates 30
```

The default main study uses 512 timepoints, one length-64 variance burst,
strengths 0.75 and 1, aligned / ±16 / ±64 / uniform placement, 200 train and
500 test cases, and 30 independent replicates. A single anchor with enough
margin for the largest jitter is shared across placements, with separate
training and test RNG streams. This fixes the older branch runner's different
test count and condition-dependent anchor. The generator implementation is
retained. Historical seed-base confirmation is still required to claim an exact
match to the paper's numerical table.

The global-summary diagnostic is stored separately. Average within a replicate,
then report means and standard errors over replicates; do not treat these as
independent archive datasets for Wilcoxon testing.

## Forecasting reduction

Save an already selected univariate series as a numeric one-dimensional `.npy` file:

```bash
interval-forecast data/series.npy --estimator d-quant --output local/forecasts/series/d-quant.csv
```

The runner supports DrCIF, QUANT, their differenced-response versions, Ridge and
Naive. It refits on expanding histories at each of the final 30 consecutive
observations, uses 99 predictor values and one target per 100-value window,
and restores differenced predictions to levels. It never trains on future
observations. The manuscript does not identify exact origins, so the final-origin
policy is explicit and must be reconciled with the original run manifest.

The 100 series IDs are recorded in `configs/datasets/tsfr100.txt`. Source download
mapping, truncation offsets, final origins, and configurations
for AutoETS, AutoARIMA, SCUM, TimeCNN/d-TimeCNN and N-BEATS have not yet been
recovered. Their deposited mean results are displayed, but a new implementation with
guessed defaults is not labelled as their reproduction. The same applies to the
multivariate LITETime-MV and PatchMTSC reference configurations.

### Batch runner over all series

`configs/datasets/tsfr100_series.csv` holds the actual values of each of the 100
series, one per line, prefixed by the series name (`<name>,v0,v1,...`). The
values are the concatenated train then test observations (each series truncated
to at most 10000 points, as in tsml-eval's split); the final 30 values of a line
are the rolling one-step origins and everything before them is history.
`wind_farms_minutely_dataset_without_missing_values_T6` is the `T6` series of the
Monash `.tsf` that tsml-eval downloads, which has no separately deposited
train/test problem.

`interval-forecast-batch` runs the reduction forecasters over that file. Unlike
the per-series `interval-forecast` above (a manual 99-predictor window), it uses
aeon's `RegressionForecaster` with the paper's `window=100`, matching the
tsml-eval pipeline, and its differenced variants match `DifferencedForecaster`
(order 1). Estimators are whatever you name; any registry regression name is
accepted, with an optional `d-` prefix, plus `ridge` and `naive`.

```bash
interval-forecast-batch --estimators quant d-quant drcif d-drcif ridge naive --dry-run
interval-forecast-batch --estimators d-drcif ridge naive --datasets m4_daily_dataset_T1
interval-forecast-batch --estimators quant d-quant drcif d-drcif ridge naive
```

It writes a per-series `origin,actual,predicted` file and manifest under
`local/forecasts_batch/<method>/`, a per-series `summary_metrics.csv`, and a
`summary_ranks.csv` of mean MSE/MAE/sMAPE ranks in the same shape as
`results/TSFR/manuscript_summary_ranks.csv`.

`--dump-problems [DIR]` additionally writes, for every series, the exact windowed
design a regressor is fitted on -- one CSV per series under `DIR/level/` and
`DIR/differenced/` (default `DIR` is `configs/datasets/tsfr_problems`). Each row
is `target_index` (the index in the original series of the value it forecasts),
`window` lag features (oldest `t-100` to newest `t-1`), then `target`; the 30
rolling problems are the rows whose `target_index` is among the final 30
positions. For the differenced files the lags and target are first differences,
and the level forecast is `target` plus the original value at `target_index - 1`.
Given only `--dump-problems` (no `--estimators`) the command emits the files and
exits without forecasting.

## Rebuild league tables

Collate predictions with the included command, which uses tsml-eval's verified
result loaders. It requires every explicitly requested dataset, estimator and
resample, checks the recorded dataset/split/resample metadata, and averages
each metric over resamples before ranking datasets:

```bash
interval-collate --task classification --results-path local/results --datasets GunPoint --estimators quant tsf --resamples 0 --output local/summary
```

Use the complete dataset and resample lists for final study tables. Then supply
the per-dataset mean matrix:

```bash
interval-league results/UCR/accuracy_mean.csv --metric Accuracy --output local/tables/univariate.md --pairwise local/tables/univariate-pvalues.csv
interval-league results/TSER/rmse_mean.csv --metric RMSE --lower-better --output local/tables/regression.md
```

Run `python tools/generate_results.py` to rebuild all four benchmark pages,
the README, dataset lists and source checksums without changing the source CSVs.
Tables rank methods **within datasets**, average the ranks and count wins
including ties. Missing scores, duplicate dataset IDs and non-finite values fail
validation; no silent intersection changes the population. Optional pairwise
tests are two-sided Wilcoxon with Holm correction over all pairs, following the
paper's general protocol. The manuscript has conflicting one-sided wording in its
univariate section; resolve this before regenerating its significance claims.
Its component ablations explicitly report uncorrected tests instead.

To extract a separate reference snapshot directly from the manuscript,
run `python tools/snapshot_paper.py /path/to/main.tex --date YYYY-MM-DD` from
the repository root. This writes to `docs/paper-tables/` and records the manuscript
hash there; it does not overwrite the benchmark tables generated from CSVs.

## Exact-reproduction status

The benchmark mean-score collections and their dataset IDs are now available.
Exact reproduction still needs raw predictions and historical run manifests.
In particular, the manuscript
still requests final aeon/tsml-eval commits. Record those separately from this
package's tested environment and imported source commit. The common 60/58 lists
come directly from the CSVs. Confirm the UCR103 list, per-resample coverage,
resource units, deep/statistical reference configurations, simulation seeds and
forecasting origins before declaring an exact reproduction. The repository
includes manuscript-summary CSVs for the forecasting ranks and both simulation
tables, but raw ablation/simulation replicates and raw sMAPE source files remain
absent. Exact historical run manifests, per-resample predictions and
forecasting origins/configurations are also unavailable.
