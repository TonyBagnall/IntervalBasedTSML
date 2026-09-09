"""Record the actual software and constructor configuration of new runs."""

from datetime import datetime, timezone
from importlib import metadata
import json
from pathlib import Path
import platform


def write_manifest(path, estimator=None, **details):
    """Write a uniquely located manifest before the corresponding experiment."""
    packages = {}
    for name in ("intervalbasedtsml", "aeon", "tsml", "tsml-eval", "numpy",
                 "scipy", "scikit-learn", "numba", "torch"):
        try:
            dist = metadata.distribution(name)
            packages[name] = {"version": dist.version}
            direct = dist.read_text("direct_url.json")
            if direct:
                packages[name]["direct_url"] = json.loads(direct)
        except metadata.PackageNotFoundError:
            packages[name] = None
    record = dict(created=datetime.now(timezone.utc).isoformat(),
                  python=platform.python_version(), platform=platform.platform(),
                  packages=packages, **details)
    if estimator is not None:
        record["estimator_class"] = f"{type(estimator).__module__}.{type(estimator).__name__}"
        record["parameters"] = estimator.get_params(deep=True)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, default=str) + "\n", encoding="utf-8")
