# Extrinsic regression

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

[Source CSVs](../../results/TSER/) | [Dataset list](../../configs/datasets/tser58.txt) | [Archive manifest](../../results/manifest.json)
