# Estimators

The public imports accept aeon's `(cases, channels, timepoints)` collection format.

| Estimator | Provider | Role |
| --- | --- | --- |
| `PULSARClassifier` | `intervalbasedtsml.classification` | Main comparison and parameterised ablations |
| `FITClassifier` | `intervalbasedtsml.classification` | Historical review; not in the main league tables |
| `PULSARRegressor` | `intervalbasedtsml.regression` | TSER comparison; the manuscript reports extreme errors on some problems |
| TSF, RISE, STSF, CIF, DrCIF, r-STSF, QUANT | `aeon.classification.interval_based` | Established classifiers |
| TSF, RISE, CIF, DrCIF, QUANT, RandomIntervalRegressor | `aeon.regression.interval_based` | Established regressors |

Imported implementations and simulation helpers come from tsml-eval commit
`2d224c0e784310daba7f5112845a24944aa1fbe2` on `ajb/simulator`.
Only internal package imports were relocated. Source hashes are in
[provenance.json](provenance.json); the BSD attribution is in [NOTICE](../NOTICE).
This identifies the imported implementation, not the unrecorded commits of the
historical paper runs. The paper discusses AQ-QUANT, TSBF and LPS, but they were
not present among the branch's interval ports and are not claimed as provided.

The experiment registry records 200 trees for the interval forests, the paper's
CIF/DrCIF settings, and 50 trees, depth 4 and 40% selection for PULSAR.
`pulsar-et`, `pulsar-ridge`, `pulsar-nopool`, `pulsar-nosel` and `pulsar-noar`
match the branch's ablations. The no-pooling variant uses depth 1: **global
pooling remains**, while regional hierarchy levels are removed.

Use the Python constructors for research outside these presets. Overrides in
the benchmark CLI are recorded and constitute a new configuration, so a reduced
tree count used for a smoke test must not be presented as a paper run.
