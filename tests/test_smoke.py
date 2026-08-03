"""Smoke test: verify the package can be imported and reports the expected version."""

import user_stream_tracker
from user_stream_tracker import __version__


def test_import_succeeds() -> None:
    """user_stream_tracker must be importable without errors."""
    assert user_stream_tracker is not None


def test_version_is_correct() -> None:
    """Package version must be 0.1.0 for PR 1 scaffold."""
    assert __version__ == "0.1.0"


def test_version_attribute_on_module() -> None:
    """__version__ must be accessible directly on the top-level module."""
    assert hasattr(user_stream_tracker, "__version__")
    assert user_stream_tracker.__version__ == "0.1.0"
