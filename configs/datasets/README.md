# Dataset manifests

These lists are generated from the deposited primary-metric CSV row IDs:

| List | Source |
| --- | --- |
| [ucr112.txt](ucr112.txt) | `results/UCR/accuracy_mean.csv` |
| [multiverse60.txt](multiverse60.txt) | `results/multiverse/accuracy_mean.csv` |
| [tser58.txt](tser58.txt) | `results/TSER/rmse_mean.csv` |
| [tsfr100.txt](tsfr100.txt) | `results/TSFR/mse_mean.csv` |

Regenerate with `python tools/generate_results.py`. The first three lists work
with `interval-benchmark --dataset-list`. They freeze the comparison population;
the CSVs do not explain other datasets' exclusions.

`tsfr100.txt` identifies forecasting series but does not recover source download
locations, truncation bounds or origin indices. Those need the original run
manifest. The UCR103 ablation list remains unavailable until its CSVs arrive.
