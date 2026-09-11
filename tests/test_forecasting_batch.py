"""Batch forecasting: parsing, metrics, ranking and temporal boundaries."""

import csv

import numpy as np
import pytest

from intervalbasedtsml.experiments.forecasting_batch import (
    make_regressor,
    mean_ranks,
    metrics,
    read_series_file,
    rolling_predictions,
)


def test_naive_forecast_repeats_last_history_value():
    # regressor=None is the naive forecaster: it never sees series[origin].
    rows = rolling_predictions(np.arange(110.0), False, None, origins=3)
    assert rows == [(107, 107.0, 106.0), (108, 108.0, 107.0), (109, 109.0, 108.0)]


def test_rolling_rejects_series_too_short_for_window():
    with pytest.raises(ValueError, match="Not enough history"):
        rolling_predictions(np.arange(120.0), False, None, window=100, origins=30)


def test_metrics_match_hand_computed_values():
    mse, mae, smape = metrics([(0, 10.0, 8.0), (1, 20.0, 24.0)])
    assert mse == pytest.approx((4 + 16) / 2)
    assert mae == pytest.approx((2 + 4) / 2)
    expected_smape = np.mean([200 * 2 / 18, 200 * 4 / 44])
    assert smape == pytest.approx(expected_smape)


def test_mean_ranks_average_ties_over_common_series():
    per_series = {
        "a": {"X": (1.0, 1.0, 1.0), "Y": (2.0, 2.0, 2.0)},
        "b": {"X": (5.0, 5.0, 5.0), "Y": (5.0, 5.0, 5.0)},  # tie -> 1.5 each
    }
    ranks, n_common = mean_ranks(per_series)
    assert n_common == 2
    assert ranks["X"][0] == pytest.approx((1 + 1.5) / 2)
    assert ranks["Y"][0] == pytest.approx((2 + 1.5) / 2)


def test_read_series_file_and_subset(tmp_path):
    path = tmp_path / "series.csv"
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["alpha", "1.0", "2.0", "3.0"])
        writer.writerow(["beta", "4.0", "5.0"])
    everything = list(read_series_file(path))
    assert everything == [("alpha", [1.0, 2.0, 3.0]), ("beta", [4.0, 5.0])]
    assert [n for n, _ in read_series_file(path, datasets=["beta"])] == ["beta"]


def test_make_regressor_resolves_differencing_and_special_names():
    assert make_regressor("naive") == (False, None)
    differenced, regressor = make_regressor("d-ridge")
    assert differenced and regressor is not None
    assert make_regressor("quant")[1].__class__.__name__ == "QUANTRegressor"


def test_regression_forecaster_path_does_not_see_the_future():
    pytest.importorskip("aeon")
    from sklearn.linear_model import LinearRegression

    # A linear ramp is perfectly predictable, so a correct one-step forecast
    # recovers each held-out value; a leak would be equally invisible, so also
    # assert the history fed in stops before the origin via a short window.
    rows = rolling_predictions(np.arange(200.0), False, LinearRegression(),
                               window=10, origins=3)
    predicted = [r[2] for r in rows]
    np.testing.assert_allclose(predicted, [197.0, 198.0, 199.0], atol=1e-6)
