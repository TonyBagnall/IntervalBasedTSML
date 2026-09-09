"""Run archive experiments with tsml-eval's standard partitions and result files."""

import argparse
import json
from pathlib import Path

from intervalbasedtsml.experiments._provenance import write_manifest
from intervalbasedtsml.experiments._registry import make_estimator


def main(argv=None):
    """Run a task over explicitly supplied datasets, estimators and resamples."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=("ucr", "multivariate", "tser", "ablation"), required=True)
    parser.add_argument("--data-path", type=Path, required=True)
    parser.add_argument("--results-path", type=Path, default=Path("local/results"))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--datasets", nargs="+")
    group.add_argument("--dataset-list", type=Path)
    parser.add_argument("--estimators", nargs="+", required=True)
    parser.add_argument("--resamples", nargs="+", type=int)
    parser.add_argument("--n-jobs", type=int, default=1)
    parser.add_argument("--parameters", default="{}", help="JSON constructor overrides for all selected estimators")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    datasets = args.datasets if args.datasets is not None else [
        line.strip() for line in args.dataset_list.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not datasets or len(set(datasets)) != len(datasets):
        parser.error("Provide a nonempty list of unique datasets.")
    for value in datasets + args.estimators:
        if value in (".", "..") or "/" in value or "\\" in value:
            parser.error("Dataset and estimator names must be single path components.")
    resamples = args.resamples if args.resamples is not None else (
        [0] if args.task == "multivariate" else list(range(30))
    )
    if not resamples or min(resamples) < 0 or len(set(resamples)) != len(resamples):
        parser.error("Resamples must be distinct nonnegative integers.")
    if args.task == "multivariate" and resamples != [0]:
        parser.error("The paper's multivariate protocol uses the original partition only (0).")
    task = "regression" if args.task == "tser" else "classification"
    overrides = json.loads(args.parameters)
    if not isinstance(overrides, dict):
        parser.error("--parameters must be a JSON object.")
    for name in args.estimators:
        for dataset in datasets:
            for resample in resamples:
                estimator = make_estimator(name, task, random_state=resample,
                                           n_jobs=args.n_jobs, **overrides)
                if args.dry_run:
                    print(args.task, name, dataset, resample, estimator)
                    continue
                prediction = args.results_path/name/"Predictions"/dataset/f"testResample{resample}.csv"
                if prediction.exists():
                    print(f"Skipping existing result: {prediction}")
                    continue
                write_manifest(prediction.with_suffix(".json"), estimator,
                               task=args.task, dataset=dataset, resample=resample,
                               protocol="original split" if resample == 0 else "tsml-eval resample",
                               overrides=overrides)
                from tsml_eval.experiments import (
                    load_and_run_classification_experiment,
                    load_and_run_regression_experiment,
                )
                runner = (load_and_run_regression_experiment if task == "regression"
                          else load_and_run_classification_experiment)
                runner(str(args.data_path), str(args.results_path), dataset, estimator,
                       **{"regressor_name" if task == "regression" else "classifier_name": name},
                       resample_id=resample, benchmark_time=False)


if __name__ == "__main__":
    main()
