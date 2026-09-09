# Multivariate classification

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

[Source CSVs](../../results/multiverse/) | [Dataset list](../../configs/datasets/multiverse60.txt) | [Archive manifest](../../results/manifest.json)
