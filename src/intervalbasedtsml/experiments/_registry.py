"""Explicit paper configurations and local estimator routing."""

from importlib import import_module

CLASSIFIERS = {
    "tsf": "TimeSeriesForestClassifier",
    "rise": "RandomIntervalSpectralEnsembleClassifier",
    "stsf": "SupervisedTimeSeriesForest",
    "cif": "CanonicalIntervalForestClassifier",
    "drcif": "DrCIFClassifier",
    "rstsf": "RSTSF",
    "quant": "QUANTClassifier",
}
REGRESSORS = {
    "tsf": "TimeSeriesForestRegressor",
    "rise": "RandomIntervalSpectralEnsembleRegressor",
    "cif": "CanonicalIntervalForestRegressor",
    "drcif": "DrCIFRegressor",
    "quant": "QUANTRegressor",
    "randomintervals": "RandomIntervalRegressor",
    "summary-intervals": "RandomIntervalRegressor",
}
ABLATIONS = {
    "pulsar-et": {"classifiers": ("extra_trees",)},
    "pulsar-ridge": {"classifiers": ("ridge",)},
    "pulsar-nopool": {"hierarchical_depth": 1},
    "pulsar-nosel": {"feature_selection_percentage": 100},
    "pulsar-noar": {"representations": ("original", "periodogram", "derivative")},
}


def make_estimator(name, task="classification", *, random_state=0, n_jobs=1, **overrides):
    """Construct an estimator, using the paper's recorded forest sizes.

    Overrides are for explicit new experiments and smoke tests. Each runner
    records the complete resulting configuration in a provenance sidecar.
    """
    name = name.lower()
    if task not in ("classification", "regression"):
        raise ValueError("task must be classification or regression")
    params = {"random_state": random_state}
    if name == "pulsar" or name in ABLATIONS:
        if task == "regression" and name in ABLATIONS:
            raise ValueError("Classification head ablations do not name regressors.")
        module = import_module(f"intervalbasedtsml.{task}")
        cls = getattr(module, "PULSARClassifier" if task == "classification" else "PULSARRegressor")
        params.update(n_estimators=50, hierarchical_depth=4, feature_selection_percentage=40)
        params.update(ABLATIONS.get(name, {}))
    elif name == "fit" and task == "classification":
        from intervalbasedtsml.classification import FITClassifier
        cls = FITClassifier
    elif name in (CLASSIFIERS if task == "classification" else REGRESSORS):
        mapping = CLASSIFIERS if task == "classification" else REGRESSORS
        cls = getattr(import_module(f"aeon.{task}.interval_based"), mapping[name])
        if name in ("tsf", "rise", "stsf", "cif", "drcif", "rstsf"):
            params.update(n_estimators=200, min_interval_length=3)
        if name == "quant":
            params.update(interval_depth=6, quantile_divisor=4)
        if name == "cif":
            params.update(att_subsample_size=8, n_intervals="sqrt", use_pycatch22=False)
        if name == "drcif":
            params.update(att_subsample_size=10, n_intervals=(4, "sqrt-div"),
                          max_interval_length=0.5, use_pycatch22=False)
        if name == "tsf":
            params["n_intervals"] = "sqrt"
        if name == "rstsf":
            params["n_intervals"] = 50
        if name == "rise":
            params["acf_lag"] = 100
        if name == "summary-intervals":
            from aeon.transformations.collection.feature_based import SevenNumberSummary
            from sklearn.ensemble import RandomForestRegressor
            params.update(features=SevenNumberSummary(),
                          estimator=RandomForestRegressor(n_estimators=500))
    elif task == "classification" and name in ("hc2", "mrhydra", "rocket", "rdst"):
        module, class_name = {
            "hc2": ("hybrid", "HIVECOTEV2"),
            "mrhydra": ("convolution_based", "MultiRocketHydraClassifier"),
            "rocket": ("convolution_based", "RocketClassifier"),
            "rdst": ("shapelet_based", "RDSTClassifier"),
        }[name]
        cls = getattr(import_module(f"aeon.classification.{module}"), class_name)
        if name == "mrhydra":
            params["n_kernels"] = 8
    else:
        raise ValueError(f"Unsupported {task} estimator: {name}")
    import inspect
    if "n_jobs" in inspect.signature(cls).parameters:
        params["n_jobs"] = n_jobs
    params.update(overrides)
    return cls(**params)
