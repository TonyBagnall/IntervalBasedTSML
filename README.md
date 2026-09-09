# IntervalBasedTSML

Code and results for **From TSF to PULSAR: A Review and Bake Off for
Interval-Based Time Series Machine Learning**, by Anthony Bagnall and Alexander
Banwell. The repository covers univariate and multivariate classification,
time-series extrinsic regression (TSER), forecasting-based regression, the
PULSAR component ablation and a controlled simulation study.

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

The benchmark league tables below reproduce the submitted manuscript tables. The repository also contains the deposited per-dataset mean CSVs for 112 UCR, 60 Multiverse, 58 TSER and 100 forecasting datasets. Each comparison uses its own matched population.

# Univariate classification

112 UCR datasets; 30 resamples. Ordered by mean accuracy rank.

Manuscript summary transcribed from table `rq1` on 2026-09-09. This reference copy is separate from the result-derived tables.

| Estimator | Accuracy | Balanced accuracy | AUROC | Log loss | Mean rank | Fit (s) | Predict (s) | Memory (MB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HC2 | 0.891 | 0.870 | 0.968 | 0.365 | 2.94 | 1236.0 | 965.8 | 751 |
| MR-Hydra | 0.884 | 0.866 | 0.913* | 4.182* | 3.34 | 17.4 | 26.1 | 808 |
| PULSAR | 0.880 | 0.859 | 0.964 | 0.523 | 3.49 | 33.8 | 36.4 | 375 |
| QUANT | 0.867 | 0.845 | 0.962 | 0.496 | 4.50 | 3.9 | 0.6 | 22 |
| DrCIF | 0.863 | 0.840 | 0.961 | 0.511 | 5.04 | 133.0 | 198.0 | 82 |
| r-STSF | 0.860 | 0.837 | 0.960 | 0.515 | 5.21 | 10.4 | 3.6 | 110 |
| CIF | 0.854 | 0.832 | 0.956 | 0.528 | 6.03 | 107.5 | 193.9 | 88 |
| STSF | 0.841 | 0.820 | 0.954 | 0.550 | 7.32 | 58.6 | 7.0 | 60 |
| RISE | 0.802 | 0.773 | 0.936 | 0.785 | 8.56 | 33.2 | 12.8 | 54 |
| TSF | 0.808 | 0.786 | 0.931 | 0.636 | 8.56 | 17.3 | 3.2 | 45 |

Lower mean rank and error are better; higher accuracy, AUROC and R-squared are better.

\* The manuscript reports hard 0/1 MR-Hydra outputs; its AUROC and log loss are not directly comparable with probability-producing methods.

[Results archive](results/README.md) | [Reproduction](docs/reproducing.md)

# Multivariate classification

60 common completed Multiverse-core datasets; original partition only.

Manuscript summary transcribed from table `multivariate` on 2026-09-09. This reference copy is separate from the result-derived tables.

| Estimator | Accuracy | Balanced accuracy | AUROC | Log loss | Mean rank | Fit (s) | Predict (s) | Memory (MB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HC2 | 0.783 | 0.742 | 0.883 | 0.545 | 4.55 | 29474.3 | 4890.2 | 6597 |
| MR-Hydra | 0.775 | 0.745 | 0.798* | 8.116* | 5.14 | 191.2 | 45.8 | 6415 |
| PULSAR | 0.772 | 0.738 | 0.858 | 0.613 | 5.51 | 358.8 | 55.3 | 1672 |
| r-STSF | 0.767 | 0.733 | 0.861 | 0.631 | 6.05 | 1856.2 | 31.0 | 7803 |
| DrCIF | 0.765 | 0.732 | 0.866 | 0.648 | 6.16 | 1854.6 | 894.0 | 350 |
| CIF | 0.767 | 0.734 | 0.873 | 0.650 | 6.17 | 2132.1 | 1153.5 | 280 |
| QUANT | 0.757 | 0.727 | 0.859 | 0.737 | 6.33 | 215.8 | 6.4 | 614 |
| STSF | 0.765 | 0.739 | 0.862 | 0.680 | 6.51 | 9124.8 | 76.4 | 596 |
| LITETime-MV | 0.736 | 0.713 | 0.837 | 1.344 | 6.60 | --** | --** | 1465 |
| PatchMTSC | 0.730 | 0.675 | 0.809 | 0.796 | 7.49 | --** | --** | 1089 |
| TSF | 0.735 | 0.704 | 0.848 | 0.987 | 7.99 | 253.3 | 27.5 | 141 |
| RISE | 0.683 | 0.624 | 0.828 | 0.922 | 9.49 | 176.5 | 33.4 | 162 |

Lower mean rank and error are better; higher accuracy, AUROC and R-squared are better.

\* The manuscript reports hard 0/1 MR-Hydra outputs; its AUROC and log loss are not directly comparable with probability-producing methods.

\*\* GPU timings are omitted in the manuscript because they are not comparable with CPU timings.

[Results archive](results/README.md) | [Reproduction](docs/reproducing.md)

# Extrinsic regression

58 TSER datasets; 30 resamples. Ordered by mean RMSE rank. Raw errors have different scales across datasets.

Manuscript summary transcribed from table `tser` on 2026-09-09. This reference copy is separate from the result-derived tables.

| Estimator | RMSE | MAE | R-squared | Mean rank | Fit (s) | Predict (s) | Memory (MB) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QUANT | 692.6 | 322.6 | 0.381 | 2.67 | 164.9 | 1.5 | 231 |
| DrCIF | 717.3 | 375.7 | 0.399 | 3.40 | 2297.2 | 280.0 | 300 |
| CIF | 725.1 | 384.4 | 0.362 | 3.91 | 1473.4 | 271.9 | 328 |
| PULSAR | 1666.1 | 523.9 | -3.0 x 10^10 | 4.43 | 338.0 | 34.9 | 3345 |
| TSF | 739.4 | 383.2 | 0.251 | 4.45 | 416.1 | 9.1 | 148 |
| SummaryInt | 764.0 | 356.4 | 0.174 | 4.93 | 1644.3 | 3.0 | 258 |
| RandInt | 764.4 | 355.9 | 0.164 | 5.91 | 662.6 | 0.9 | 151 |
| RISE | 751.1 | 413.8 | 0.263 | 6.29 | 538.1 | 10.2 | 151 |

Lower mean rank and error are better; higher accuracy, AUROC and R-squared are better.

PULSAR's extreme errors on a few datasets dominate its mean RMSE and R-squared. Its middling rank does not imply reliable regression performance.

[Results archive](results/README.md) | [Reproduction](docs/reproducing.md)

# Forecasting-based regression

100 series; 30 rolling one-step origins. All columns are mean ranks (lower is better).

Manuscript summary transcribed from table `tsfr` on 2026-09-09. This reference copy is separate from the result-derived tables.

| Estimator | MSE rank | MAE rank | sMAPE rank |
| --- | --- | --- | --- |
| d-DrCIF | 4.34 | 4.01 | 4.47 |
| d-QUANT | 4.67 | 4.36 | 4.71 |
| SCUM | 4.67 | 4.87 | 4.62 |
| Ridge | 5.17 | 5.43 | 5.51 |
| AutoETS | 6.00 | 5.87 | 5.76 |
| AutoARIMA | 6.00 | 5.90 | 5.81 |
| QUANT | 6.22 | 6.33 | 6.29 |
| Naive | 6.62 | 6.03 | 5.37 |
| d-TimeCNN | 7.26 | 7.35 | 7.67 |
| DrCIF | 7.33 | 7.84 | 7.63 |
| N-BEATS | 8.52 | 8.60 | 8.74 |
| TimeCNN | 11.20 | 11.42 | 11.40 |

Lower mean rank and error are better; higher accuracy, AUROC and R-squared are better.

The d- prefix means prediction of the next change, added to the last observed level. No significance claim follows from the rank order alone.

[Results archive](results/README.md) | [Reproduction](docs/reproducing.md)

# PULSAR ablation

103 UCR datasets; 30 resamples. Ordered by mean accuracy. Comparisons against QUANT use uncorrected p-values.

Manuscript summary transcribed from table `pulsar_ablation` on 2026-09-09. This reference copy is separate from the result-derived tables.

| Variant | Element removed | Accuracy | Delta QUANT | W-L-T | p (uncorrected) |
| --- | --- | --- | --- | --- | --- |
| PULSAR | -- | 0.8769 | +0.0129 | 78--21--4 | 3 x 10^-8 |
| no-AR | autoregressive repr. | 0.8748 | +0.0108 | 75--24--4 | 5 x 10^-8 |
| no-selection | Fisher-score selection | 0.8723 | +0.0083 | 73--26--4 | 6 x 10^-6 |
| no-pooling | hierarchical pooling | 0.8689 | +0.0049 | 60--39--4 | 0.043 |
| extratrees-head | the ridge head | 0.8685 | +0.0045 | 56--40--7 | 0.083 |
| QUANT | -- | 0.8640 | -- | -- | -- |
| ridge-head | the extra-trees head | 0.8604 | -0.0036 | 45--55--3 | 0.57 |
| DrCIF | -- | 0.8595 | -- | -- | -- |

Lower mean rank and error are better; higher accuracy, AUROC and R-squared are better.

[Results archive](results/README.md) | [Reproduction](docs/reproducing.md)

# Alignment simulation

30 independent paired replicates per condition. Accuracy is reported separately for each strength and placement; Global is a non-localising whole-series reference, not a competitor.

Manuscript summary transcribed from table `sim_alignment` on 2026-09-09. This reference copy is separate from the result-derived tables.

| Strength | Placement | QUANT | TSF | r-STSF | PULSAR | ROCKET | Global |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.75 | aligned | 0.847 | 0.863 | 0.873 | 0.859 | 0.685 | 0.666 |
|  | J=L/4 | 0.833 | 0.855 | 0.859 | 0.847 | 0.674 | 0.665 |
|  | J=L | 0.776 | 0.813 | 0.806 | 0.798 | 0.663 | 0.667 |
|  | uniform | 0.687 | 0.728 | 0.687 | 0.705 | 0.628 | 0.662 |
| 1.00 | aligned | 0.945 | 0.960 | 0.960 | 0.956 | 0.844 | 0.792 |
|  | J=L/4 | 0.945 | 0.955 | 0.958 | 0.952 | 0.837 | 0.793 |
|  | J=L | 0.893 | 0.928 | 0.923 | 0.926 | 0.834 | 0.793 |
|  | uniform | 0.818 | 0.875 | 0.840 | 0.869 | 0.802 | 0.792 |

Lower mean rank and error are better; higher accuracy, AUROC and R-squared are better.

[Results archive](../../results/README.md) | [Reproduction](../reproducing.md)

# Simulation ablation

Strength 1; 30 paired replicates. Accuracy and loss of accuracy on displacement; standard errors in parentheses. The paper reports conditions rather than an overall league ranking.

Manuscript summary transcribed from table `sim_ablation` on 2026-09-09. This reference copy is separate from the result-derived tables.

| Variant | Element removed | Aligned | Uniform | Loss |
| --- | --- | --- | --- | --- |
| PULSAR | -- | 0.957 (0.002) | 0.869 (0.004) | 0.088 (0.004) |
| no-pooling | hierarchical pooling | 0.910 (0.003) | 0.878 (0.003) | 0.032 (0.004) |
| no-selection | Fisher-score selection | 0.956 (0.002) | 0.870 (0.004) | 0.086 (0.004) |
| no-AR | autoregressive repr. | 0.957 (0.002) | 0.870 (0.004) | 0.088 (0.004) |
| extratrees-head | the ridge head | 0.957 (0.002) | 0.876 (0.003) | 0.081 (0.004) |
| ridge-head | the extra-trees head | 0.942 (0.003) | 0.835 (0.004) | 0.107 (0.005) |
| TSF | -- | 0.961 (0.002) | 0.875 (0.003) | 0.086 (0.004) |
| ROCKET | -- | 0.851 (0.004) | 0.802 (0.003) | 0.050 (0.005) |

Lower mean rank and error are better; higher accuracy, AUROC and R-squared are better.

[Results archive](../../results/README.md) | [Reproduction](../reproducing.md)

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
