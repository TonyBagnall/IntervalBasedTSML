"""Build league tables from complete, matched per-dataset results."""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata, wilcoxon


def load_scores(path):
    """Read a tsml-eval mean matrix (dataset column followed by estimators).

    Missing, duplicate and non-finite values are errors: silently intersecting
    available results would change the benchmark population.
    """
    import csv

    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        header = next(csv.reader(stream), [])
    if len(header) < 3 or len(set(header[1:])) != len(header[1:]):
        raise ValueError("Expected dataset plus at least two unique estimator columns.")
    scores = pd.read_csv(path, index_col=0)
    if scores.empty or scores.index.has_duplicates or scores.index.isna().any():
        raise ValueError("Dataset names must be nonempty and unique.")
    scores = scores.apply(pd.to_numeric, errors="raise")
    if not np.isfinite(scores.to_numpy()).all():
        raise ValueError("Every estimator must have a finite score on every dataset.")
    return scores


def league_table(scores, *, lower_better=False):
    """Rank within datasets, then average; ties receive average ranks."""
    values = scores.to_numpy(dtype=float)
    if values.size == 0 or not np.isfinite(values).all():
        raise ValueError("Scores must be a nonempty finite matrix.")
    ranks = rankdata(values if lower_better else -values, axis=1)
    best = values.min(axis=1) if lower_better else values.max(axis=1)
    table = pd.DataFrame({
        "Estimator": scores.columns,
        "Mean rank": ranks.mean(axis=0),
        "Mean score": values.mean(axis=0),
        "Wins (including ties)": (values == best[:, None]).sum(axis=0),
        "Datasets": len(scores),
    })
    return table.sort_values(["Mean rank", "Estimator"], kind="stable").reset_index(drop=True)


def pairwise_tests(scores):
    """Two-sided Wilcoxon tests with Holm correction across all method pairs."""
    rows = []
    for i, left in enumerate(scores.columns):
        for right in scores.columns[i + 1:]:
            difference = scores[left].to_numpy() - scores[right].to_numpy()
            p = 1.0 if np.all(difference == 0) else wilcoxon(difference).pvalue
            rows.append([left, right, float(p)])
    result = pd.DataFrame(rows, columns=["Estimator A", "Estimator B", "p raw"])
    if not rows:
        return result.assign(**{"p Holm": []})
    order = np.argsort(result["p raw"].to_numpy())
    adjusted = np.minimum(1, np.maximum.accumulate(
        result["p raw"].to_numpy()[order] * np.arange(len(rows), 0, -1)
    ))
    result["p Holm"] = 0.0
    result.loc[order, "p Holm"] = adjusted
    return result


def markdown_table(table):
    """Render Markdown without requiring an optional table-formatting package."""
    def cell(value):
        if isinstance(value, (float, np.floating)):
            return f"{value:.4f}"
        return str(value).replace("|", "\\|").replace("\n", " ")
    lines = ["| " + " | ".join(map(cell, table.columns)) + " |",
             "| " + " | ".join(["---"] * len(table.columns)) + " |"]
    lines.extend("| " + " | ".join(map(cell, row)) + " |"
                 for row in table.itertuples(index=False, name=None))
    return "\n".join(lines) + "\n"


def main(argv=None):
    """Generate a league table and optionally corrected pairwise tests."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", type=Path, help="Dataset-by-estimator mean CSV")
    parser.add_argument("--metric", required=True)
    parser.add_argument("--lower-better", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pairwise", type=Path)
    args = parser.parse_args(argv)
    scores = load_scores(args.scores)
    table = league_table(scores, lower_better=args.lower_better)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    direction = "lower" if args.lower_better else "higher"
    args.output.write_text(
        f"# {args.metric} league table\n\n"
        f"{len(scores)} matched datasets; {direction} score is better. "
        "Lower mean rank is better; tied scores receive average ranks.\n\n"
        + markdown_table(table), encoding="utf-8",
    )
    if args.pairwise:
        args.pairwise.parent.mkdir(parents=True, exist_ok=True)
        pairwise_tests(scores).to_csv(args.pairwise, index=False)


if __name__ == "__main__":
    main()
