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
