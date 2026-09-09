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

[Results archive](../../results/README.md) | [Reproduction](../reproducing.md)
