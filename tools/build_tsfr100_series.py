"""Assemble the consolidated forecasting series file from prepared problems.

Reads the dataset IDs in ``configs/datasets/tsfr100.txt`` and, for each one,
concatenates its prepared ``<name>_TRAIN.csv`` and ``<name>_TEST.csv`` (in that
order) into a single one-dimensional series. The concatenated series is written
to ``configs/datasets/tsfr100_series.csv`` with one series per line, prefixed by
its name:

    <name>,<v0>,<v1>,...,<vN>

The final 30 values of each line are the rolling one-step origins used by
``interval-forecast-batch``; everything before them is the available history.

The prepared per-series problems live outside this repository (they are derived
from the Monash forecasting archive under its own licence). Supply their
location with ``--data-root``; each series is expected at
``<data-root>/<name>/<name>_TRAIN.csv`` and ``..._TEST.csv``, each a single
column of values with a one-line header. IDs with no prepared problem are
reported and skipped, so the output can legitimately contain fewer than 100
lines; re-run once the missing problems are available.
"""

import argparse
import csv
from pathlib import Path


def _read_values(path):
    """Return the numeric values of a single-column CSV, skipping its header."""
    with path.open("r", newline="", encoding="utf-8") as stream:
        rows = [line.strip() for line in stream]
    values = []
    for cell in rows[1:]:  # first line is the column header
        if cell == "":
            continue
        values.append(float(cell))
    return values


def build_series(name, data_root):
    """Concatenate the TRAIN then TEST values of one prepared problem."""
    folder = data_root / name
    train = _read_values(folder / f"{name}_TRAIN.csv")
    test = _read_values(folder / f"{name}_TEST.csv")
    return train + test


def read_ids(list_path):
    """Return the non-comment, non-blank dataset IDs from a newline list."""
    ids = []
    for raw in list_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            ids.append(line)
    return ids


def main(argv=None):
    """Write the consolidated, name-prefixed series file."""
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-root",
        type=Path,
        required=True,
        help="Directory of prepared problems (<data-root>/<name>/<name>_TRAIN.csv).",
    )
    parser.add_argument(
        "--ids",
        type=Path,
        default=repo_root / "configs" / "datasets" / "tsfr100.txt",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "configs" / "datasets" / "tsfr100_series.csv",
    )
    args = parser.parse_args(argv)

    ids = read_ids(args.ids)
    written, missing = 0, []
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        for name in ids:
            if not (args.data_root / name / f"{name}_TRAIN.csv").exists():
                missing.append(name)
                continue
            series = build_series(name, args.data_root)
            writer.writerow([name, *(repr(value) for value in series)])
            written += 1

    print(f"Wrote {written} series to {args.output}")
    if missing:
        print(f"Missing prepared problems for {len(missing)} ID(s): {missing}")


if __name__ == "__main__":
    main()
