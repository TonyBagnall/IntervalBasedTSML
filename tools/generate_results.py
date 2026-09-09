"""Regenerate benchmark tables and dataset manifests from the deposited CSVs."""

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

from intervalbasedtsml.results import load_scores, league_table, markdown_table

ROOT = Path(__file__).resolve().parents[1]
STUDIES = [
    ("UCR", "univariate", "Univariate classification", "accuracy", 112, 10, "ucr112.txt"),
    ("multiverse", "multivariate", "Multivariate classification", "accuracy", 60, 12, "multiverse60.txt"),
    ("TSER", "regression", "Extrinsic regression", "rmse", 58, 8, "tser58.txt"),
    ("TSFR", "forecasting", "Forecasting-based regression", "mse", 100, 12, "tsfr100.txt"),
]


def build_study(folder, primary, expected_shape):
    """Validate all metric matrices and align their explicit identifiers."""
    frames = {p.stem.removesuffix("_mean"): load_scores(p)
              for p in sorted(folder.glob("*_mean.csv"))}
    reference = frames[primary]
    if reference.shape != expected_shape:
        raise ValueError(f"Unexpected coverage for {folder}: {reference.shape}")
    for name, frame in frames.items():
        if set(frame.index) != set(reference.index) or set(frame.columns) != set(reference.columns):
            raise ValueError(f"Mismatched dataset or estimator IDs: {folder}/{name}")
        frames[name] = frame.loc[reference.index, reference.columns]
    table = league_table(reference, lower_better=primary != "accuracy")
    order = table["Estimator"]
    table = table[["Estimator", "Mean rank", "Wins (including ties)"]]
    metrics = (["accuracy", "balacc", "auroc", "logloss"] if primary == "accuracy"
               else ["rmse", "mae", "r2"] if primary == "rmse" else ["mae", "rmse"])
    labels = {"accuracy": "Accuracy", "balacc": "Balanced accuracy", "auroc": "AUROC",
              "logloss": "Log loss", "rmse": "RMSE", "mae": "MAE", "r2": "R-squared"}
    for metric in metrics:
        if primary == "mse":
            ranks = rankdata(frames[metric].to_numpy(), axis=1).mean(axis=0)
            values = dict(zip(reference.columns, ranks))
            table[labels[metric] + " rank"] = [values[name] for name in order]
        else:
            table[labels[metric]] = frames[metric].mean().loc[order].to_numpy()
    if primary == "mse":
        table = table.rename(columns={"Mean rank": "MSE rank"})
    else:
        for metric, label, divisor in [("fittime", "Fit (s)", 1000),
                                      ("predicttime", "Predict (s)", 1000),
                                      ("memoryusage", "Memory (MiB)", 1024**2)]:
            values = frames[metric]
            # Never average a sentinel, or silently average only available datasets.
            table[label] = [
                "unavailable" if (values[name] < 0).any() else f"{values[name].mean()/divisor:.1f}"
                for name in order
            ]
            if folder.name == "multiverse" and metric != "memoryusage":
                table.loc[table.Estimator.isin(["LITETime-MV", "PatchMTSC"]), label] = "GPU: omitted"
    return frames, table


def main():
    """Write deterministic Markdown and provenance without changing source CSVs."""
    manifest = {"source": "deposited per-dataset mean CSVs", "studies": {},
                "historical_run_commits": None,
                "protocol_evidence": "Resample/origin counts come from the manuscript; mean CSVs cannot verify them.",
                "unit_interpretation": "Timing milliseconds and memory bytes, inferred from tsml-eval conventions and manuscript scale; original headers are absent."}
    sections = []
    for directory, slug, title, primary, n, k, dataset_file in STUDIES:
        folder = ROOT/"results"/directory
        frames, table = build_study(folder, primary, (n, k))
        scores = frames[primary]
        notes = "Ranks are computed within each dataset, with average ranks for ties, then averaged across datasets. Wins include ties. Rank order alone does not establish statistical significance.\n"
        if primary == "accuracy":
            notes += "\nMR-Hydra AUROC and log loss are not directly comparable with probability-producing methods: the manuscript describes hard 0/1 outputs.\n"
        if directory == "UCR":
            notes += "\nFit time and memory are unavailable (-1 in the source) for CIF, DrCIF, RISE, STSF and TSF. Prediction times are taken from these CSVs and differ from some draft values.\n"
        if directory == "multiverse":
            notes += "\nGPU fit/prediction times for LITETime-MV and PatchMTSC are omitted from this CPU comparison.\n"
        if primary == "rmse":
            notes += "\nRaw errors have different target scales. PULSAR's extreme errors on a few datasets dominate its mean RMSE and R-squared.\n"
        if primary == "mse":
            notes += "\nsMAPE is absent from the deposited files and cannot be reconstructed from MAPE or aggregate errors. RMSE ranks are shown instead; no sMAPE values are inferred. Forecast timing/memory columns contain many zeros and are not presented as a cost comparison.\n"
        else:
            notes += "\nTime is displayed in seconds (source / 1,000), memory in MiB (source / 1,048,576). Source units are inferred from tsml-eval conventions and manuscript scale, since mean CSVs have no unit metadata.\n"
        protocol = ("Original partition, according to the manuscript." if directory == "multiverse"
                    else "30 rolling origins, according to the manuscript." if primary == "mse"
                    else "30 resamples, according to the manuscript.")
        heading = f"{n} datasets; {k} estimators. {protocol} Scores come from the deposited per-dataset means; the underlying resamples/origins are not included.\n"
        content = f"# {title}\n\n{heading}\n" + markdown_table(table) + "\n" + notes
        content += f"\n[Source CSVs](../../results/{directory}/) | [Dataset list](../../configs/datasets/{dataset_file}) | [Archive manifest](../../results/manifest.json)\n"
        (ROOT/f"docs/league-tables/{slug}.md").write_text(content, encoding="utf-8")
        sections.append(f"### {title}\n\n{heading}\n" + markdown_table(table) + "\n" + notes)
        (ROOT/"configs/datasets"/dataset_file).write_text("\n".join(map(str, scores.index)) + "\n", encoding="utf-8")
        files = {}
        for p in sorted(folder.glob("*.csv")):
            df = frames[p.stem.removesuffix("_mean")]
            files[p.name] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                             "negative_values": int((df < 0).sum().sum()),
                             "zero_values": int((df == 0).sum().sum())}
        manifest["studies"][directory] = {"datasets": list(scores.index),
                                           "estimators": list(scores.columns),
                                           "primary_metric": primary, "files": files}
    (ROOT/"results/manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    path = ROOT/"README.md"
    readme = path.read_text(encoding="utf-8")
    before = readme.split("## Paper results", 1)[0]
    after = readme.split("## Install and use", 1)[1]
    intro = ("## Paper results\n\nThe four benchmark league tables below are generated from the 40 deposited CSVs in "
             "[results/](results/README.md). The archive covers 112 UCR, 60 Multiverse, 58 TSER and 100 forecasting datasets. "
             "Each table uses its own matched population.\n\n"
             "[PULSAR ablations](docs/league-tables/ablations.md), [alignment simulations](docs/league-tables/simulation.md) "
             "and [simulation ablations](docs/league-tables/simulation-ablation.md) remain manuscript snapshots; their CSVs have not been deposited.\n\n")
    path.write_text(before + intro + "\n".join(sections) + "\n## Install and use" + after, encoding="utf-8")
    print("Regenerated four league tables, four dataset lists and the CSV checksum manifest.")


if __name__ == "__main__":
    main()
