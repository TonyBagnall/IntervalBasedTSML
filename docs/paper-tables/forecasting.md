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

[Results archive](../../results/README.md) | [Reproduction](../reproducing.md)
