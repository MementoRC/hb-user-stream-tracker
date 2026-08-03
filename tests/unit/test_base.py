"""Unit tests for the UserStreamTrackerBase scaffold placeholder."""

import pytest

from user_stream_tracker.base import UserStreamTrackerBase


@pytest.mark.unit
def test_user_stream_tracker_base_importable() -> None:
    """UserStreamTrackerBase must be importable from user_stream_tracker.base."""
    assert UserStreamTrackerBase is not None


@pytest.mark.unit
def test_user_stream_tracker_base_instantiable() -> None:
    """UserStreamTrackerBase must be instantiable with no arguments."""
    tracker = UserStreamTrackerBase()
    assert isinstance(tracker, UserStreamTrackerBase)
