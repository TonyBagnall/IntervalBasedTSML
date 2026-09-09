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

[Results archive](../../results/README.md) | [Reproduction](../reproducing.md)
