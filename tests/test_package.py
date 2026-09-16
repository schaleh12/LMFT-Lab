"""Sanity checks for the repository's Python package layout."""

from pathlib import Path

import gft_lab


def test_imports_local_package():
    """Ensure tests import this checkout's package from src."""
    expected = Path(__file__).resolve().parents[1] / "src" / "gft_lab" / "__init__.py"
    assert Path(gft_lab.__file__).resolve() == expected
