"""Sanity checks for the repository's Python package layout."""

from pathlib import Path

import lmft_lab


def test_imports_local_package():
    """Ensure tests import this checkout's package from src."""
    expected = Path(__file__).resolve().parents[1] / "src" / "lmft_lab" / "__init__.py"
    assert Path(lmft_lab.__file__).resolve() == expected
