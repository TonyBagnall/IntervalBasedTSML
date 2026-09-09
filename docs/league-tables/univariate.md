# Univariate classification

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

[Source CSVs](../../results/UCR/) | [Dataset list](../../configs/datasets/ucr112.txt) | [Archive manifest](../../results/manifest.json)
