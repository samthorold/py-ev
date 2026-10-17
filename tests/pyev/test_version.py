import tomllib
from pathlib import Path

import pyev

PYPROJECT = Path(__file__).parents[2] / "pyproject.toml"


def test_version_matches_pyproject() -> None:
    with PYPROJECT.open("rb") as f:
        expected = tomllib.load(f)["project"]["version"]

    assert pyev.__version__ == expected
