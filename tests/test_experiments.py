"""Check source relocation and temporal evaluation boundaries."""

import numpy as np
import pytest
from sklearn.base import BaseEstimator, RegressorMixin, clone

from intervalbasedtsml.experiments._registry import make_estimator
from intervalbasedtsml.experiments.forecasting import rolling_predictions
from intervalbasedtsml.experiments.simulation import generate_pair


class LastChange(RegressorMixin, BaseEstimator):
    """Assert that each training target is a change in the observed history."""

    def fit(self, X, y):
        np.testing.assert_allclose(y, 1)
        self.last_training_value_ = X[-1, 0, -1]
        return self

    def predict(self, X):
        assert X[0, 0, -1] == self.last_training_value_ + 1
        return np.ones(len(X))


def test_rolling_targets_and_level_restoration():
    rows = rolling_predictions(np.arange(110.0), LastChange(), origins=3, difference=True)
    assert rows == [(107, 107.0, 107.0), (108, 108.0, 108.0), (109, 109.0, 109.0)]
    assert rolling_predictions(np.arange(110.0), None, origins=1)[0] == (109, 109.0, 108.0)


def test_pairing_and_independent_test_split():
    aligned, ap = generate_pair(1, "aligned", 2)
    uniform, up = generate_pair(1, "uniform", 2)
    assert ap["anchor"] == up["anchor"]
    assert aligned[0].shape == (200, 1, 512)
    assert aligned[2].shape == (500, 1, 512)
    assert not np.array_equal(aligned[0], aligned[2][:200])
    np.testing.assert_array_equal(aligned[0], generate_pair(1, "aligned", 2)[0][0])


@pytest.mark.parametrize("task,names", [
    ("classification", ["tsf", "rise", "cif", "drcif", "stsf", "rstsf", "quant", "pulsar", "fit"]),
    ("regression", ["tsf", "rise", "cif", "drcif", "quant", "pulsar", "randomintervals", "summary-intervals"]),
])
def test_paper_estimators_construct_and_clone(task, names):
    for name in names:
        estimator = make_estimator(name, task)
        assert type(clone(estimator)) is type(estimator)
        assert "tsml_eval._wip" not in type(estimator).__module__


def test_pulsar_regressor_fits_after_relocation():
    model = make_estimator("pulsar", "regression", representations=("original",),
                           interval_lengths=(3,), max_dilation=1,
                           n_estimators=3, hierarchical_depth=1)
    rng = np.random.RandomState(1)
    X = rng.normal(size=(12, 1, 20))
    y = X.mean(axis=(1, 2))
    prediction = model.fit(X, y).predict(X[:3])
    assert prediction.shape == (3,)
    assert np.isfinite(prediction).all()


def test_fit_classifier_preserves_string_labels():
    model = make_estimator("fit", n_estimators=2, cv_n_estimators=1,
                           cv_repeats=1, cv_folds=2)
    rng = np.random.RandomState(2)
    X = rng.normal(size=(12, 1, 20))
    y = np.array(["low"] * 6 + ["high"] * 6)
    X[6:] += 3
    probabilities = model.fit(X, y).predict_proba(X)
    np.testing.assert_allclose(probabilities.sum(axis=1), 1)
    assert set(model.predict(X)) <= set(y)


def test_collation_requires_all_resamples_and_matching_metadata(tmp_path):
    from tsml_eval.evaluation.storage.classifier_results import ClassifierResults
    from intervalbasedtsml.experiments.collate import collate

    path = tmp_path / "A" / "Predictions" / "dataset" / "testResample0.csv"
    path.parent.mkdir(parents=True)
    result = ClassifierResults(dataset_name="dataset", classifier_name="A",
                               split="TEST", resample_id=0,
                               class_labels=np.array([0, 1]), predictions=np.array([0, 1]),
                               probabilities=np.array([[0.8, 0.2], [0.1, 0.9]]))
    result.save_to_file(path.parent.as_posix())
    frames = collate(tmp_path, ["dataset"], ["A"], [0], "classification")
    assert frames["accuracy"].loc["dataset", "A"] == 1
    with pytest.raises(FileNotFoundError):
        collate(tmp_path, ["dataset"], ["A"], [0, 1], "classification")
    result.dataset_name = "different"
    result.save_to_file(path.parent.as_posix())
    with pytest.raises(ValueError, match="metadata"):
        collate(tmp_path, ["dataset"], ["A"], [0], "classification")
