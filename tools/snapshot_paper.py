"""Refresh draft summary tables from the author's LaTeX manuscript (no CSV import)."""

import argparse
import hashlib
import json
from pathlib import Path


SPECS = [
    ("rq1", "univariate", "Univariate classification",
     "112 UCR datasets; 30 resamples. Ordered by mean accuracy rank.",
     ["Estimator", "Accuracy", "Balanced accuracy", "AUROC", "Log loss", "Mean rank", "Fit (s)", "Predict (s)", "Memory (MB)"]),
    ("multivariate", "multivariate", "Multivariate classification",
     "60 common completed Multiverse-core datasets; original partition only.",
     ["Estimator", "Accuracy", "Balanced accuracy", "AUROC", "Log loss", "Mean rank", "Fit (s)", "Predict (s)", "Memory (MB)"]),
    ("tser", "regression", "Extrinsic regression",
     "58 TSER datasets; 30 resamples. Ordered by mean RMSE rank. Raw errors have different scales across datasets.",
     ["Estimator", "RMSE", "MAE", "R-squared", "Mean rank", "Fit (s)", "Predict (s)", "Memory (MB)"]),
    ("tsfr", "forecasting", "Forecasting-based regression",
     "100 series; 30 rolling one-step origins. All columns are mean ranks (lower is better).",
     ["Estimator", "MSE rank", "MAE rank", "sMAPE rank"]),
    ("pulsar_ablation", "ablations", "PULSAR ablation",
     "103 UCR datasets; 30 resamples. Ordered by mean accuracy. Comparisons against QUANT use uncorrected p-values.",
     ["Variant", "Element removed", "Accuracy", "Delta QUANT", "W-L-T", "p (uncorrected)"]),
    ("sim_alignment", "simulation", "Alignment simulation",
     "30 independent paired replicates per condition. Accuracy is reported separately for each strength and placement; the Floor column is a global-summary diagnostic, not a competitor.",
     ["Strength", "Placement", "QUANT", "TSF", "r-STSF", "PULSAR", "ROCKET", "RDST", "Floor"]),
    ("sim_ablation", "simulation-ablation", "Simulation ablation",
     "Strength 1; five paired replicates. Accuracy and loss of accuracy on displacement; standard errors in parentheses. The paper reports conditions rather than an overall league ranking.",
     ["Variant", "Element removed", "Aligned", "Uniform", "Loss"]),
]


def clean(value):
    """Convert the small set of LaTeX constructs in the summary tables."""
    value = value.strip().replace(r"$^\dagger$", "*").replace(r"$^\ddagger$", "**")
    return (value.replace(r"\times", " x ").replace("$", "")
            .replace("{", "").replace("}", "").replace("---", "--"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    destination = Path("docs/paper-tables")
    destination.mkdir(parents=True, exist_ok=True)
    raw = args.manuscript.read_bytes()
    paper = raw.decode("utf-8")
    blocks = []
    for label, slug, title, description, headers in SPECS:
        block = paper.split(r"\label{tab:" + label + "}", 1)[1]
        body = block.split(r"\end{tabular}", 1)[0].split(r"\midrule", 1)[1]
        rows = [[clean(cell) for cell in line.split(r"\\")[0].split("&")]
                for line in body.splitlines() if "&" in line]
        if any(len(row) != len(headers) for row in rows):
            raise ValueError(f"Unexpected column count in {label}")
        if slug == "ablations":
            rows.sort(key=lambda row: -float(row[2]))
        table = "| " + " | ".join(headers) + " |\n"
        table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
        table += "".join("| " + " | ".join(row) + " |\n" for row in rows)
        notes = "\nLower mean rank and error are better; higher accuracy, AUROC and R-squared are better.\n"
        if slug in ("univariate", "multivariate"):
            notes += "\n\\* The draft reports hard 0/1 MR-Hydra outputs; its AUROC and log loss are not directly comparable with probability-producing methods.\n"
        if slug == "multivariate":
            notes += "\n\\*\\* GPU timings are omitted in the draft because they are not comparable with CPU timings.\n"
        if slug == "regression":
            notes += "\nPULSAR's extreme errors on a few datasets dominate its mean RMSE and R-squared. Its middling rank does not imply reliable regression performance.\n"
        if slug == "forecasting":
            notes += "\nThe d- prefix means prediction of the next change, added to the last observed level. No significance claim follows from the rank order alone.\n"
        content = f"# {title}\n\n{description}\n\n"
        content += (f"Draft snapshot transcribed from manuscript table `{label}` on {args.date}. "
                    "These values have not yet been reconciled with the cleaned CSV archive. "
                    "Displayed ranks are rounded; apparent ties are not broken using rounded means.\n\n")
        content += table + notes + "\n[Results archive](../../results/README.md) | [Reproduction](../reproducing.md)\n"
        (destination / f"{slug}.md").write_text(content, encoding="utf-8", newline="\n")
        if not slug.startswith("simulation"):
            blocks.append(f"### {title}\n\n{description}\n\n" + table + notes)
    (destination / "paper-snapshot.json").write_text(json.dumps({
        "title": "Interval-Based Time Series Classification: A Historical, Design and Empirical Review",
        "source": args.manuscript.name, "snapshot_date": args.date,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "status": "work in progress; CSV reconciliation pending",
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
