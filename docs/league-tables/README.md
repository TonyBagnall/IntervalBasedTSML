# Paper league tables

The four benchmark tables are recalculated from deposited per-dataset mean CSVs.
Their full-precision ranks determine the ordering. Ablation and simulation
tables remain manuscript snapshots, pending their CSVs.

| Comparison | Coverage | Primary ordering |
| --- | --- | --- |
| [Univariate](univariate.md) | 112 UCR datasets, 30 resamples | Mean accuracy rank |
| [Multivariate](multivariate.md) | 60 common Multiverse-core datasets, original split | Mean accuracy rank |
| [Regression](regression.md) | 58 TSER datasets, 30 resamples | Mean RMSE rank |
| [Forecasting](forecasting.md) | 100 series, 30 rolling origins | Mean MSE rank |
| [Ablations](ablations.md) | 103 UCR datasets, 30 resamples | Mean accuracy |
| [Alignment simulation](simulation.md) | 30 paired population replicates per condition | Accuracy by strength and placement |
| [Simulation ablation](simulation-ablation.md) | 5 paired replicates, strength 1 | Aligned/uniform accuracy and displacement loss |

The [Multiverse repository](https://github.com/aeon-toolkit/multiverse) has its
own benchmark populations and league table; its results should not be substituted
for this paper's 60-dataset comparison.

`python tools/generate_results.py` rebuilds the benchmark pages, README,
dataset lists and source checksum manifest. `interval-league` builds individual
tables from mean matrices, rejecting incomplete inputs rather than dropping datasets.
It optionally computes two-sided Wilcoxon tests with Holm correction over every
pair in the table. Average ranks use average ranks for ties.
