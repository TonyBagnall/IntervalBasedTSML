# Simulation ablation

Strength 1; 30 paired replicates. Accuracy and loss of accuracy on displacement; standard errors in parentheses. The paper reports conditions rather than an overall league ranking.

Manuscript summary transcribed from table `sim_ablation` on 2026-09-09. This reference copy is separate from the result-derived tables.

| Variant | Element removed | Aligned | Uniform | Loss |
| --- | --- | --- | --- | --- |
| PULSAR | -- | 0.957 (0.002) | 0.869 (0.004) | 0.088 (0.004) |
| no-pooling | hierarchical pooling | 0.910 (0.003) | 0.878 (0.003) | 0.032 (0.004) |
| no-selection | Fisher-score selection | 0.956 (0.002) | 0.870 (0.004) | 0.086 (0.004) |
| no-AR | autoregressive repr. | 0.957 (0.002) | 0.870 (0.004) | 0.088 (0.004) |
| extratrees-head | the ridge head | 0.957 (0.002) | 0.876 (0.003) | 0.081 (0.004) |
| ridge-head | the extra-trees head | 0.942 (0.003) | 0.835 (0.004) | 0.107 (0.005) |
| TSF | -- | 0.961 (0.002) | 0.875 (0.003) | 0.086 (0.004) |
| ROCKET | -- | 0.851 (0.004) | 0.802 (0.003) | 0.050 (0.005) |

Lower mean rank and error are better; higher accuracy, AUROC and R-squared are better.

[Results archive](../../results/README.md) | [Reproduction](../reproducing.md)
