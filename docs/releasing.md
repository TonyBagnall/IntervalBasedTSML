# Releasing the package

The proposed PyPI distribution and import name is `intervalbasedtsml`.
Name availability and ownership have not been established, and no package has
been published. Runtime dependencies use release ranges; they are not presented
as a lock of the paper's historical environment.

1. Reconcile historical manifests and results as described in
   [reproducing.md](reproducing.md). Add the public paper URL/DOI and results
   archive DOI to the README and citation metadata once assigned. Repository URLs are
   already recorded in the project metadata.
2. Install `.[experiments,dev]` in a fresh virtual environment, run
   `python -m pytest`, then `python -m build` and `python -m twine check dist/*`.
3. Inspect both distributions: estimators and helpers belong in the wheel;
   result CSVs and local datasets do not. The source distribution includes the
   tests, documentation, configuration guidance and license notices.
4. Install the built wheel in a clean environment, run the documented imports
   and a small experiment. Record the tested dependency versions. CI performs
   the package checks on Python 3.12 and 3.13.
5. Replace the development version in `pyproject.toml`, `__init__.py` and
   `CITATION.cff`, add release notes, build again and publish through the chosen
   PyPI account or trusted publishing configuration when ready.

No publishing workflow is enabled. Results are versioned in Git separately from
the package; choose a durable archive DOI for the final paper release.
