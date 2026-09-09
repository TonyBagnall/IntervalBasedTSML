# Forecasting-based regression

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

[Source CSVs](../../results/TSFR/) | [Dataset list](../../configs/datasets/tsfr100.txt) | [Archive manifest](../../results/manifest.json)
