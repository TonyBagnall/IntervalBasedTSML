"""Check benchmark ranking and input integrity."""

import numpy as np
import pandas as pd
import pytest

from intervalbasedtsml.results import league_table, load_scores, pairwise_tests


def test_rank_per_dataset_instead_of_rank_of_means():
    scores = pd.DataFrame({"A": [100, 2, 2], "B": [0, 3, 3]})
    table = league_table(scores)
    assert table["Estimator"].tolist() == ["B", "A"]
    assert table.iloc[0]["Mean rank"] == pytest.approx(4 / 3)
    assert league_table(scores, lower_better=True).iloc[0]["Estimator"] == "A"


def test_ties_and_identical_pairwise_results():
    scores = pd.DataFrame({"A": [1, 2, 3], "B": [1, 2, 3], "C": [0, 0, 0]})
    table = league_table(scores)
    assert table.iloc[0]["Mean rank"] == 1.5
    assert table.iloc[0]["Wins (including ties)"] == 3
    pairs = pairwise_tests(scores)
    assert len(pairs) == 3
    assert pairs.iloc[0]["p raw"] == 1
    assert np.all(pairs["p Holm"] >= pairs["p raw"])


@pytest.mark.parametrize("content", [
    "dataset,A,B\nx,1,\n", "dataset,A,B\nx,1,2\nx,2,3\n",
    "dataset,A,A\nx,1,2\n", "dataset,A,B\nx,inf,2\n",
])
def test_incomplete_or_ambiguous_archive_fails(tmp_path, content):
    source = tmp_path / "scores.csv"
    source.write_text(content)
    with pytest.raises(ValueError):
        load_scores(source)
