"""Batch rolling one-step forecasting over the consolidated 100-series file.

A cut-down version of the tsml-eval forecasting pipeline. For every requested
estimator and every series in ``configs/datasets/tsfr100_series.csv`` this:

1. reads the series' values (the final ``origins`` of which are the held-out
   rolling one-step targets);
2. for each of the final ``origins`` positions, refits on the history strictly
   before that position and forecasts one step ahead. Windowing is delegated to
   aeon's :class:`~aeon.forecasting.RegressionForecaster`, which turns the
   history into ``(n_windows, window)`` lag/target pairs and feeds them to the
   wrapped regressor -- exactly the reduction tsml-eval applies, with the
   paper's ``window=100``;
3. writes a per-series prediction file (``origin,actual,predicted``) with a
   provenance sidecar, and accumulates MSE / MAE / sMAPE.

Differenced (``d-``) estimators forecast the first difference and add the last
observed level back, matching tsml-eval's ``DifferencedForecaster`` (order 1).
``ridge`` wraps ``RidgeCV`` and ``naive`` repeats the last observed value.

After all runs it writes ``summary_metrics.csv`` (one row per method/series) and
``summary_ranks.csv`` (mean rank per method and metric, lower is better), the
latter in the same shape as ``results/TSFR/manuscript_summary_ranks.csv``.

Estimators are whatever you pass to ``--estimators``; any regression name the
experiment registry understands is accepted, optionally with a ``d-`` prefix,
plus ``ridge`` and ``naive``.
"""

import argparse
import csv
from pathlib import Path

import numpy as np
from sklearn.base import clone
from sklearn.linear_model import RidgeCV

from intervalbasedtsml.experiments._provenance import write_manifest
from intervalbasedtsml.experiments._registry import make_estimator

# Display labels for the summary tables; unknown names fall back to upper-case.
_LABELS = {
    "quant": "QUANT", "d-quant": "d-QUANT", "drcif": "DrCIF", "d-drcif": "d-DrCIF",
    "cif": "CIF", "tsf": "TSF", "rise": "RISE", "ridge": "Ridge", "naive": "Naive",
    "pulsar": "PULSAR", "d-pulsar": "d-PULSAR",
}


def _label(name):
    return _LABELS.get(name, name.upper())


def make_regressor(name, *, seed=0, n_jobs=1):
    """Resolve a CLI estimator name to (is_differenced, regressor_or_None).

    ``None`` marks the naive last-value forecaster, which uses no regressor.
    """
    differenced = name.startswith("d-")
    base = name[2:] if differenced else name
    if base == "naive":
        return differenced, None
    if base == "ridge":
        return differenced, RidgeCV(alphas=np.logspace(-3, 3, 10))
    return differenced, make_estimator(base, "regression", random_state=seed, n_jobs=n_jobs)


def rolling_predictions(series, differenced, regressor, *, window=100, origins=30):
    """Refit at each of the final ``origins`` positions and forecast one step.

    The history for a position contains only observations strictly before it, so
    no future value is ever seen during fitting.
    """
    series = np.asarray(series, dtype=float)
    if series.ndim != 1 or not np.isfinite(series).all():
        raise ValueError("series must be one-dimensional and finite")
    shortest_history = len(series) - origins
    if origins < 1 or shortest_history - int(differenced) <= window:
        raise ValueError(
            "Not enough history: need more than "
            f"{window} observations before the first of {origins} origins."
        )
    # RegressionForecaster is imported lazily so the module imports without aeon.
    from aeon.forecasting import RegressionForecaster

    rows = []
    for origin in range(shortest_history, len(series)):
        history = series[:origin]
        if regressor is None:
            prediction = float(history[-1])
        elif differenced:
            forecaster = RegressionForecaster(window=window, regressor=clone(regressor))
            prediction = float(forecaster.forecast(np.diff(history))) + float(history[-1])
        else:
            forecaster = RegressionForecaster(window=window, regressor=clone(regressor))
            prediction = float(forecaster.forecast(history))
        rows.append((origin, float(series[origin]), prediction))
    return rows


def metrics(rows):
    """Return (MSE, MAE, sMAPE) over one series' rolling predictions."""
    actual = np.array([r[1] for r in rows], dtype=float)
    predicted = np.array([r[2] for r in rows], dtype=float)
    error = actual - predicted
    denominator = np.abs(actual) + np.abs(predicted)
    smape_terms = np.where(denominator == 0, 0.0, 200.0 * np.abs(error) / denominator)
    return (
        float(np.mean(error**2)),
        float(np.mean(np.abs(error))),
        float(np.mean(smape_terms)),
    )


def read_series_file(path, datasets=None):
    """Yield (name, values) from the name-prefixed consolidated series file."""
    wanted = set(datasets) if datasets else None
    with Path(path).open("r", newline="", encoding="utf-8") as stream:
        for record in csv.reader(stream):
            if not record:
                continue
            name = record[0]
            if wanted is not None and name not in wanted:
                continue
            yield name, [float(value) for value in record[1:]]


def mean_ranks(per_series):
    """Mean rank (lower better, ties averaged) of each method for every metric.

    ``per_series`` maps series -> {method: (mse, mae, smape)}; only series scored
    by every method contribute, so the ranking uses one matched population.
    """
    methods = sorted({m for scores in per_series.values() for m in scores})
    complete = [s for s, scores in per_series.items() if len(scores) == len(methods)]
    ranks = {m: [0.0, 0.0, 0.0] for m in methods}
    for series in complete:
        scores = per_series[series]
        for metric_index in range(3):
            values = np.array([scores[m][metric_index] for m in methods])
            order = values.argsort()
            metric_ranks = np.empty(len(methods))
            metric_ranks[order] = np.arange(1, len(methods) + 1)
            # Average tied ranks so equal errors share the same position.
            for value in np.unique(values):
                tie = values == value
                metric_ranks[tie] = metric_ranks[tie].mean()
            for method, rank in zip(methods, metric_ranks):
                ranks[method][metric_index] += rank
    n = max(len(complete), 1)
    return {m: [r / n for r in totals] for m, totals in ranks.items()}, len(complete)


def main(argv=None):
    """Run the requested forecasters over the consolidated series file."""
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--estimators", nargs="+", required=True,
                        help="e.g. quant d-quant drcif d-drcif ridge naive")
    parser.add_argument("--series-file", type=Path,
                        default=repo_root / "configs" / "datasets" / "tsfr100_series.csv")
    parser.add_argument("--output", type=Path, default=repo_root / "local" / "forecasts_batch")
    parser.add_argument("--datasets", nargs="+", default=None,
                        help="Optional subset of series names (default: all).")
    parser.add_argument("--origins", type=int, default=30)
    parser.add_argument("--window", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--n-jobs", type=int, default=1)
    parser.add_argument("--overwrite", action="store_true",
                        help="Recompute per-series prediction files that already exist.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the planned runs and exit without forecasting.")
    args = parser.parse_args(argv)

    series = list(read_series_file(args.series_file, args.datasets))
    if not series:
        parser.error("No matching series found in the series file.")
    if args.dry_run:
        print(f"{len(args.estimators)} estimators x {len(series)} series, "
              f"origins={args.origins}, window={args.window}")
        for name in args.estimators:
            print(f"  {name} -> {_label(name)}")
        return

    args.output.mkdir(parents=True, exist_ok=True)
    per_series = {name: {} for name, _ in series}
    metric_rows = []
    for estimator_name in args.estimators:
        label = _label(estimator_name)
        differenced, regressor = make_regressor(estimator_name, seed=args.seed,
                                                 n_jobs=args.n_jobs)
        estimator_dir = args.output / label
        estimator_dir.mkdir(parents=True, exist_ok=True)
        write_manifest(estimator_dir / "manifest.json", regressor,
                       estimator_name=estimator_name, differenced=differenced,
                       window=args.window, origins=args.origins,
                       origin_policy="final consecutive observations")
        for name, values in series:
            prediction_path = estimator_dir / f"{name}.csv"
            if prediction_path.exists() and not args.overwrite:
                rows = [(int(r[0]), float(r[1]), float(r[2]))
                        for r in list(csv.reader(prediction_path.open()))[1:]]
            else:
                rows = rolling_predictions(values, differenced, regressor,
                                           window=args.window, origins=args.origins)
                with prediction_path.open("w", newline="", encoding="utf-8") as stream:
                    writer = csv.writer(stream)
                    writer.writerow(["origin", "actual", "predicted"])
                    writer.writerows(rows)
            mse, mae, smape = metrics(rows)
            per_series[name][label] = (mse, mae, smape)
            metric_rows.append((label, name, mse, mae, smape))
            print(f"{label:10s} {name:55s} MSE={mse:.4g} MAE={mae:.4g} sMAPE={smape:.4g}")

    with (args.output / "summary_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["method", "series", "mse", "mae", "smape"])
        writer.writerows(metric_rows)

    ranks, n_common = mean_ranks(per_series)
    with (args.output / "summary_ranks.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["method", "MSE", "MAE", "sMAPE"])
        for method in sorted(ranks, key=lambda m: ranks[m][0]):
            writer.writerow([method, *(f"{r:.2f}" for r in ranks[method])])

    print(f"\nMean ranks over {n_common} series scored by every method "
          f"(-> {args.output / 'summary_ranks.csv'}):")
    print(f"{'method':10s} {'MSE':>6s} {'MAE':>6s} {'sMAPE':>6s}")
    for method in sorted(ranks, key=lambda m: ranks[m][0]):
        mse_rank, mae_rank, smape_rank = ranks[method]
        print(f"{method:10s} {mse_rank:6.2f} {mae_rank:6.2f} {smape_rank:6.2f}")


if __name__ == "__main__":
    main()
