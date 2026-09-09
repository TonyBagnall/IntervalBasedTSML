"""Collate a complete grid of tsml-eval predictions into league-table inputs."""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

METRICS = {
    "classification": {"accuracy": "accuracy", "balanced_accuracy": "balanced_accuracy",
                       "auroc": "auroc_score", "log_loss": "log_loss"},
    "regression": {"rmse": "root_mean_squared_error", "mae": "mean_absolute_error",
                   "r2": "r2_score"},
}


def collate(results_path, datasets, estimators, resamples, task):
    """Require every expected cell and verify recorded dataset, split and resample."""
    from tsml_eval.evaluation.storage.classifier_results import load_classifier_results
    from tsml_eval.evaluation.storage.regressor_results import load_regressor_results

    if task not in METRICS:
        raise ValueError("Unsupported task")
    for values in (datasets, estimators, resamples):
        if not values or len(set(values)) != len(values):
            raise ValueError("Datasets, estimators and resamples must be nonempty and unique.")
    loader = load_classifier_results if task == "classification" else load_regressor_results
    frames = {metric: pd.DataFrame(index=pd.Index(datasets, name="dataset"),
                                  columns=estimators, dtype=float) for metric in METRICS[task]}
    for dataset in datasets:
        for estimator in estimators:
            records = []
            for resample in resamples:
                path = Path(results_path)/estimator/"Predictions"/dataset/f"testResample{resample}.csv"
                record = loader(str(path))
                if (record.dataset_name != dataset or record.resample_id != resample
                        or record.split.lower() != "test"):
                    raise ValueError(f"Result metadata does not match the expected cell: {path}")
                records.append(record)
            for metric, attr in METRICS[task].items():
                values = [getattr(record, attr) for record in records]
                if not np.isfinite(values).all():
                    raise ValueError(f"Non-finite {metric}: {estimator}/{dataset}")
                frames[metric].loc[dataset, estimator] = np.mean(values)
    return frames


def main(argv=None):
    """Write one per-dataset mean matrix per metric after completeness validation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=list(METRICS), required=True)
    parser.add_argument("--results-path", type=Path, required=True)
    parser.add_argument("--datasets", nargs="+", required=True)
    parser.add_argument("--estimators", nargs="+", required=True)
    parser.add_argument("--resamples", nargs="+", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    frames = collate(args.results_path, args.datasets, args.estimators, args.resamples, args.task)
    args.output.mkdir(parents=True, exist_ok=True)
    for metric, frame in frames.items():
        frame.to_csv(args.output/f"{metric}_mean.csv")


if __name__ == "__main__":
    main()
