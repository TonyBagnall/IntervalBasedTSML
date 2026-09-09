"""Rolling one-step interval regression with 99 predictors per window."""

import argparse
import csv
from pathlib import Path

import numpy as np
from sklearn.base import clone
from sklearn.linear_model import RidgeCV

from intervalbasedtsml.experiments._provenance import write_manifest
from intervalbasedtsml.experiments._registry import make_estimator


def rolling_predictions(series, estimator, *, origins=30, difference=False, tabular=False):
    """Refit at each of the final origins, using only observations before it.

    For differenced responses, input windows remain levels; the target is
    y[t] - y[t-1] and predictions are restored by adding the last observed level.
    """
    series = np.asarray(series, dtype=float)
    if series.ndim != 1 or not np.isfinite(series).all():
        raise ValueError("series must be one-dimensional and finite")
    if origins < 1 or len(series) - origins < 100:
        raise ValueError("Need at least 100 observations before the first origin.")
    rows = []
    for origin in range(len(series) - origins, len(series)):
        history = series[:origin]
        windows = np.lib.stride_tricks.sliding_window_view(history, 100)
        X, y = windows[:, :99].copy(), windows[:, 99].copy()
        if difference:
            y -= X[:, -1]
        query = history[-99:].reshape(1, -1)
        if estimator is None:
            prediction = history[-1]
        else:
            model = clone(estimator)
            model.fit(X if tabular else X[:, None, :], y)
            prediction = float(model.predict(query if tabular else query[:, None, :])[0])
            if difference:
                prediction += history[-1]
        rows.append((origin, float(series[origin]), float(prediction)))
    return rows


def main(argv=None):
    """Forecast a supplied, already selected Monash series stored as a 1D .npy file."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("series", type=Path)
    parser.add_argument("--estimator", choices=["quant", "d-quant", "drcif", "d-drcif", "ridge", "naive"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--origins", type=int, default=30)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--n-jobs", type=int, default=1)
    args = parser.parse_args(argv)
    if args.output.exists():
        parser.error("Output already exists; choose a new path for a new run.")
    series = np.load(args.series, allow_pickle=False)
    name = args.estimator.removeprefix("d-")
    model = (None if name == "naive" else RidgeCV() if name == "ridge" else
             make_estimator(name, "regression", random_state=args.seed, n_jobs=args.n_jobs))
    rows = rolling_predictions(series, model, origins=args.origins,
                               difference=args.estimator.startswith("d-"), tabular=name == "ridge")
    write_manifest(args.output.with_suffix(".json"), model, series=str(args.series),
                   origins=args.origins, window_length=100, estimator_name=args.estimator,
                   origin_policy="final consecutive observations")
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["origin", "actual", "predicted"])
        writer.writerows(rows)


if __name__ == "__main__":
    main()
