# PULSAR ablation

103 UCR datasets; 30 resamples. Ordered by mean accuracy. Comparisons against QUANT use uncorrected p-values.

Draft snapshot transcribed from manuscript table `pulsar_ablation` on 2026-09-09. These values have not yet been reconciled with the cleaned CSV archive. Displayed ranks are rounded; apparent ties are not broken using rounded means.

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

[Results archive](../../results/README.md) | [Reproduction](../reproducing.md)
