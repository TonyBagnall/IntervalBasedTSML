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

[Results archive](../../results/README.md) | [Reproduction](../reproducing.md)
