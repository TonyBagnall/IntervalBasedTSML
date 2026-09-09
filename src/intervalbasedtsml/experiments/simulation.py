"""Run the paper's paired variance-burst alignment experiment."""

import argparse
import csv
from pathlib import Path

import numpy as np

from intervalbasedtsml.experiments._provenance import write_manifest
from intervalbasedtsml.experiments._registry import make_estimator
from intervalbasedtsml.simulation._protocol import draw_anchor, simulate_protocol_problem


def generate_pair(strength, placement, replicate, *, seed_base=0, n_train=200, n_test=500):
    """Generate independent train/test samples with an anchor shared across placements."""
    if placement not in ("aligned", "quarter", "full", "uniform"):
        raise ValueError("Unknown placement")
    # The margin is the maximum jitter in ALL four conditions, including aligned.
    anchor = draw_anchor(512, 64, 64, np.random.RandomState(seed_base + 7919 * replicate))
    params = dict(mechanism="scale", length=64, strength=strength,
                  jitter={"aligned": 0, "quarter": 16, "full": 64, "uniform": 0}[placement],
                  uniform_location=placement == "uniform", anchor=anchor)
    train = simulate_protocol_problem(n_cases=n_train, random_state=seed_base + 2 * replicate, **params)
    test = simulate_protocol_problem(n_cases=n_test, random_state=seed_base + 2 * replicate + 1, **params)
    return (*train, *test), params


def main(argv=None):
    """Write predictions and a separate whole-series diagnostic for each replicate."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-path", type=Path, default=Path("local/simulation"))
    parser.add_argument("--estimators", nargs="+", default=["quant", "tsf", "rstsf", "pulsar", "rocket"])
    parser.add_argument("--strengths", nargs="+", type=float, default=[0.75, 1.0])
    parser.add_argument("--placements", nargs="+", choices=["aligned", "quarter", "full", "uniform"],
                        default=["aligned", "quarter", "full", "uniform"])
    parser.add_argument("--replicates", type=int, default=30)
    parser.add_argument("--seed-base", type=int, default=0)
    parser.add_argument("--n-jobs", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    if args.replicates < 1 or args.seed_base < 0:
        parser.error("Replicates must be positive and seed-base nonnegative.")
    for strength in args.strengths:
        for replicate in range(args.replicates):
            for placement in args.placements:
                condition = f"scale_a{strength:g}_{placement}"
                if args.dry_run:
                    print(condition, replicate, *args.estimators, "global-summary (diagnostic)")
                    continue
                data, params = generate_pair(strength, placement, replicate, seed_base=args.seed_base)
                X_train, y_train, X_test, y_test = data
                from tsml_eval.experiments import run_classification_experiment
                from intervalbasedtsml.simulation._diagnostics import GlobalSummaryDiagnostic
                for name in args.estimators:
                    classifier = make_estimator(name, random_state=replicate, n_jobs=args.n_jobs)
                    target = args.results_path/name/"Predictions"/condition/f"testResample{replicate}.csv"
                    if target.exists():
                        continue
                    write_manifest(target.with_suffix(".json"), classifier,
                                   condition=params, replicate=replicate,
                                   seed_base=args.seed_base, n_train=200, n_test=500,
                                   sampling="independent population replicate")
                    run_classification_experiment(
                        X_train, y_train, X_test, y_test, classifier,
                        str(args.results_path), classifier_name=name,
                        dataset_name=condition, resample_id=replicate, benchmark_time=False,
                    )
                diagnostic = GlobalSummaryDiagnostic(random_state=replicate).fit(X_train, y_train)
                target = args.results_path/"diagnostics"/condition/f"replicate{replicate}.csv"
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists():
                    with target.open("w", encoding="utf-8", newline="") as stream:
                        writer = csv.writer(stream)
                        writer.writerow(["actual", "predicted"])
                        writer.writerows(zip(y_test, diagnostic.predict(X_test)))


if __name__ == "__main__":
    main()
