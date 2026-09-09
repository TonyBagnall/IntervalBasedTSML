# Simulation ablation

Strength 1; five paired replicates. Accuracy and loss of accuracy on displacement; standard errors in parentheses. The paper reports conditions rather than an overall league ranking.

Draft snapshot transcribed from manuscript table `sim_ablation` on 2026-09-09. These values have not yet been reconciled with the cleaned CSV archive. Displayed ranks are rounded; apparent ties are not broken using rounded means.

| Variant | Element removed | Aligned | Uniform | Loss |
| --- | --- | --- | --- | --- |
| PULSAR | -- | 0.961 (0.005) | 0.881 (0.011) | 0.080 (0.011) |
| no-pooling | hierarchical pooling | 0.922 (0.006) | 0.887 (0.011) | 0.034 (0.013) |
| no-selection | Fisher-score selection | 0.959 (0.005) | 0.879 (0.011) | 0.080 (0.012) |
| no-AR | autoregressive repr. | 0.960 (0.004) | 0.882 (0.010) | 0.078 (0.010) |
| extratrees-head | the ridge head | 0.960 (0.004) | 0.893 (0.005) | 0.067 (0.005) |
| ridge-head | the extra-trees head | 0.950 (0.008) | 0.845 (0.011) | 0.105 (0.018) |
| TSF | -- | 0.962 (0.004) | 0.884 (0.009) | 0.078 (0.011) |
| ROCKET | -- | 0.850 (0.004) | 0.801 (0.011) | 0.048 (0.013) |

Lower mean rank and error are better; higher accuracy, AUROC and R-squared are better.

[Results archive](../../results/README.md) | [Reproduction](../reproducing.md)
