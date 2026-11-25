"""Smoke test: verify the package can be imported and reports the expected version."""

import re

import user_stream_tracker
from user_stream_tracker import __version__


def test_import_succeeds() -> None:
    """user_stream_tracker must be importable without errors."""
    assert user_stream_tracker is not None


def test_version_is_correct() -> None:
    """Package version must be a semantic version string."""
    assert re.fullmatch(r"\d+\.\d+\.\d+", __version__)


def test_version_attribute_on_module() -> None:
    """__version__ must be accessible directly on the top-level module."""
    assert hasattr(user_stream_tracker, "__version__")
    assert user_stream_tracker.__version__ == __version__
