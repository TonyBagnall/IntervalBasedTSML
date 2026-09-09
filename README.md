# IntervalBasedTSML

Code and results for **Interval-Based Time Series Classification: A Historical,
Design and Empirical Review**, by Anthony Bagnall and Alexander Banwell.
The paper and this repository are works in progress.

Built on **[aeon](https://www.aeon-toolkit.org/)**, the time series machine
learning toolkit, with **[tsml](https://github.com/time-series-machine-learning/tsml-py)**
and **[tsml-eval](https://github.com/time-series-machine-learning/tsml-eval)**.
The **[Multiverse archive](https://github.com/aeon-toolkit/multiverse)** supplies
the multivariate benchmark and inspires this repository's league tables and
results organisation. Please cite aeon and Multiverse when using their software
or data, alongside this study.

[League tables](docs/league-tables/README.md) | [Reproduce experiments](docs/reproducing.md) --
[Estimator guide](docs/estimators.md) | [Results files](results/README.md) --
[Release guide](docs/releasing.md)

## Paper results

The four benchmark league tables below are generated from the 40 deposited CSVs in [results/](results/README.md). The archive covers 112 UCR, 60 Multiverse, 58 TSER and 100 forecasting datasets. Each table uses its own matched population.

[PULSAR ablations](docs/league-tables/ablations.md), [alignment simulations](docs/league-tables/simulation.md) and [simulation ablations](docs/league-tables/simulation-ablation.md) remain manuscript snapshots; their CSVs have not been deposited.

### Univariate classification

112 datasets; 10 estimators. 30 resamples, according to the manuscript. Scores come from the deposited per-dataset means; the underlying resamples/origins are not included.

| Estimator | Mean rank | Wins (including ties) | Accuracy | Balanced accuracy | AUROC | Log loss | Fit (s) | Predict (s) | Memory (MiB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HC2 | 2.9464 | 43 | 0.8906 | 0.8697 | 0.9678 | 0.3655 | 1236.0 | 965.8 | 716.7 |
| MR-Hydra | 3.3393 | 44 | 0.8840 | 0.8658 | 0.9132 | 4.1819 | 17.4 | 26.1 | 770.8 |
| PULSAR | 3.4821 | 18 | 0.8797 | 0.8590 | 0.9644 | 0.5233 | 33.8 | 36.4 | 357.7 |
| QUANT | 4.5045 | 9 | 0.8670 | 0.8450 | 0.9617 | 0.4959 | 3.9 | 0.6 | 20.7 |
| DrCIF | 5.0402 | 5 | 0.8627 | 0.8400 | 0.9609 | 0.5108 | unavailable | 195.5 | unavailable |
| r-STSF | 5.2143 | 12 | 0.8598 | 0.8375 | 0.9603 | 0.5147 | 10.4 | 3.6 | 105.0 |
| CIF | 6.0312 | 6 | 0.8542 | 0.8318 | 0.9563 | 0.5280 | unavailable | 204.4 | unavailable |
| STSF | 7.3214 | 7 | 0.8415 | 0.8204 | 0.9541 | 0.5504 | unavailable | 7.6 | unavailable |
| RISE | 8.5580 | 4 | 0.8022 | 0.7725 | 0.9357 | 0.7849 | unavailable | 14.6 | unavailable |
| TSF | 8.5625 | 4 | 0.8075 | 0.7859 | 0.9311 | 0.6359 | unavailable | 3.8 | unavailable |

Ranks are computed within each dataset, with average ranks for ties, then averaged across datasets. Wins include ties. Rank order alone does not establish statistical significance.

MR-Hydra AUROC and log loss are not directly comparable with probability-producing methods: the manuscript describes hard 0/1 outputs.

Fit time and memory are unavailable (-1 in the source) for CIF, DrCIF, RISE, STSF and TSF. Prediction times are taken from these CSVs and differ from some draft values.

Time is displayed in seconds (source / 1,000), memory in MiB (source / 1,048,576). Source units are inferred from tsml-eval conventions and manuscript scale, since mean CSVs have no unit metadata.

### Multivariate classification

60 datasets; 12 estimators. Original partition, according to the manuscript. Scores come from the deposited per-dataset means; the underlying resamples/origins are not included.

| Estimator | Mean rank | Wins (including ties) | Accuracy | Balanced accuracy | AUROC | Log loss | Fit (s) | Predict (s) | Memory (MiB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HC2 | 4.5500 | 21 | 0.7828 | 0.7416 | 0.8833 | 0.5449 | 29474.3 | 4890.2 | 6596.5 |
| MR-Hydra | 5.1417 | 15 | 0.7748 | 0.7446 | 0.7980 | 8.1164 | 191.2 | 45.8 | 6415.3 |
| PULSAR | 5.5083 | 6 | 0.7717 | 0.7385 | 0.8583 | 0.6135 | 358.8 | 55.3 | 1671.7 |
| r-STSF | 6.0500 | 6 | 0.7669 | 0.7329 | 0.8605 | 0.6311 | 1856.2 | 31.0 | 7803.3 |
| DrCIF | 6.1583 | 4 | 0.7655 | 0.7316 | 0.8656 | 0.6483 | 1854.6 | 894.0 | 350.2 |
| CIF | 6.1750 | 7 | 0.7670 | 0.7343 | 0.8728 | 0.6500 | 2132.1 | 1153.5 | 280.1 |
| QUANT | 6.3333 | 5 | 0.7571 | 0.7266 | 0.8589 | 0.7372 | 215.8 | 6.4 | 613.9 |
| STSF | 6.5083 | 7 | 0.7650 | 0.7387 | 0.8625 | 0.6796 | 9124.8 | 76.4 | 596.2 |
| LITETime-MV | 6.6000 | 15 | 0.7364 | 0.7130 | 0.8374 | 1.3438 | GPU: omitted | GPU: omitted | 1465.4 |
| PatchMTSC | 7.4917 | 5 | 0.7298 | 0.6748 | 0.8090 | 0.7960 | GPU: omitted | GPU: omitted | 1089.0 |
| TSF | 7.9917 | 6 | 0.7345 | 0.7041 | 0.8476 | 0.9867 | 253.3 | 27.5 | 141.4 |
| RISE | 9.4917 | 4 | 0.6825 | 0.6238 | 0.8277 | 0.9219 | 176.5 | 33.4 | 161.6 |

Ranks are computed within each dataset, with average ranks for ties, then averaged across datasets. Wins include ties. Rank order alone does not establish statistical significance.

MR-Hydra AUROC and log loss are not directly comparable with probability-producing methods: the manuscript describes hard 0/1 outputs.

GPU fit/prediction times for LITETime-MV and PatchMTSC are omitted from this CPU comparison.

Time is displayed in seconds (source / 1,000), memory in MiB (source / 1,048,576). Source units are inferred from tsml-eval conventions and manuscript scale, since mean CSVs have no unit metadata.

### Extrinsic regression

58 datasets; 8 estimators. 30 resamples, according to the manuscript. Scores come from the deposited per-dataset means; the underlying resamples/origins are not included.

| Estimator | Mean rank | Wins (including ties) | RMSE | MAE | R-squared | Fit (s) | Predict (s) | Memory (MiB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QUANT | 2.6724 | 17 | 692.6180 | 322.5867 | 0.3811 | 164.9 | 1.5 | 220.4 |
| DrCIF | 3.3966 | 7 | 717.2552 | 375.6932 | 0.3993 | 2297.2 | 280.0 | 285.9 |
| CIF | 3.9138 | 9 | 725.1109 | 384.3833 | 0.3616 | 1473.4 | 271.9 | 312.9 |
| PULSAR | 4.4310 | 18 | 1666.0976 | 523.8747 | -30365000518.3865 | 338.0 | 34.9 | 3190.0 |
| TSF | 4.4483 | 2 | 739.4347 | 383.2141 | 0.2507 | 416.1 | 9.1 | 140.7 |
| SummaryIntervals | 4.9310 | 1 | 764.0488 | 356.4460 | 0.1742 | 1644.3 | 3.0 | 245.8 |
| RandomIntervals | 5.9138 | 0 | 764.4000 | 355.9189 | 0.1641 | 662.6 | 0.9 | 144.5 |
| RISE | 6.2931 | 4 | 751.0875 | 413.8285 | 0.2628 | 538.1 | 10.2 | 143.8 |

Ranks are computed within each dataset, with average ranks for ties, then averaged across datasets. Wins include ties. Rank order alone does not establish statistical significance.

Raw errors have different target scales. PULSAR's extreme errors on a few datasets dominate its mean RMSE and R-squared.

Time is displayed in seconds (source / 1,000), memory in MiB (source / 1,048,576). Source units are inferred from tsml-eval conventions and manuscript scale, since mean CSVs have no unit metadata.

### Forecasting-based regression

100 datasets; 12 estimators. 30 rolling origins, according to the manuscript. Scores come from the deposited per-dataset means; the underlying resamples/origins are not included.

| Estimator | MSE rank | Wins (including ties) | MAE rank | RMSE rank |
| --- | --- | --- | --- | --- |
| d-DrCIF | 4.3450 | 10 | 4.0150 | 4.3450 |
| SCUM | 4.6700 | 13 | 4.8700 | 4.6700 |
| d-QUANT | 4.6750 | 12 | 4.3550 | 4.6750 |
| Ridge | 5.1700 | 25 | 5.4300 | 5.1700 |
| AutoETS | 5.9950 | 6 | 5.8650 | 5.9950 |
| AutoARIMA | 6.0000 | 7 | 5.9000 | 6.0000 |
| QUANT | 6.2250 | 12 | 6.3250 | 6.2250 |
| Naive | 6.6150 | 7 | 6.0250 | 6.6150 |
| d-TimeCNN | 7.2600 | 1 | 7.3500 | 7.2600 |
| DrCIF | 7.3250 | 8 | 7.8450 | 7.3250 |
| NBeats | 8.5200 | 4 | 8.6000 | 8.5200 |
| TimeCNN | 11.2000 | 0 | 11.4200 | 11.2000 |

Ranks are computed within each dataset, with average ranks for ties, then averaged across datasets. Wins include ties. Rank order alone does not establish statistical significance.

sMAPE is absent from the deposited files and cannot be reconstructed from MAPE or aggregate errors. RMSE ranks are shown instead; no sMAPE values are inferred. Forecast timing/memory columns contain many zeros and are not presented as a cost comparison.

## Install and use

Python 3.12-3.14. Install from a checkout (the package is not yet published):

```bash
python -m pip install -e ".[experiments,dev]"
```

```python
from intervalbasedtsml.classification import PULSARClassifier, FITClassifier
from intervalbasedtsml.regression import PULSARRegressor
from aeon.classification.interval_based import QUANTClassifier
```

PULSAR and FIT are included from the `ajb/simulator` branch of tsml-eval.
The established interval estimators come from aeon. See [source provenance](docs/provenance.json)
and [NOTICE](NOTICE) for the imported commit, file hashes and attribution.

## Repository layout

```text
src/intervalbasedtsml/   Installable estimators, experiments and results analysis
configs/                Study protocols and dataset manifest guidance
docs/                   League tables, reproduction and release documentation
results/                Reserved tracked archive for cleaned result CSVs
tests/                  Estimator, protocol and analysis checks
local/                  Ignored outputs from development and new experiments
```

Result files belong in the repository archive, separately from the PyPI wheel.
See [CITATION.cff](CITATION.cff) for the work-in-progress software citation and
[reproduction status](docs/reproducing.md) for what is still needed to match the
historical runs exactly.
