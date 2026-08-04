"""Tests for user_stream_tracker.tracker — ported from hummingbot's
test_user_stream_tracker.py, rewritten to pytest-native style (no unittest).
"""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from user_stream_tracker.data_source import UserStreamTrackerDataSource
from user_stream_tracker.tracker import UserStreamTracker


class MockUserStreamTrackerDataSource(UserStreamTrackerDataSource):
    """Mock implementation for testing"""

    def __init__(self) -> None:
        super().__init__()
        self._mock_last_recv_time = 123.456

    @property
    def last_recv_time(self) -> float:
        return self._mock_last_recv_time

    async def _connected_websocket_assistant(self):
        return AsyncMock()

    async def _subscribe_channels(self, websocket_assistant):
        pass

    async def listen_for_user_stream(self, output: asyncio.Queue):
        # Mock implementation that puts test data
        await output.put({"test": "data"})

    async def stop(self):
        pass


@pytest.fixture
def mock_data_source() -> MockUserStreamTrackerDataSource:
    return MockUserStreamTrackerDataSource()


@pytest.fixture
def tracker(mock_data_source: MockUserStreamTrackerDataSource) -> UserStreamTracker:
    return UserStreamTracker(mock_data_source)


def test_init(
    tracker: UserStreamTracker, mock_data_source: MockUserStreamTrackerDataSource
) -> None:
    assert isinstance(tracker._user_stream, asyncio.Queue)
    assert tracker._data_source == mock_data_source
    assert tracker._user_stream_tracking_task is None


def test_logger_creation(tracker: UserStreamTracker) -> None:
    logger = tracker.logger()
    assert logger is not None
    assert logger == tracker._ust_logger


def test_data_source_property(
    tracker: UserStreamTracker, mock_data_source: MockUserStreamTrackerDataSource
) -> None:
    assert tracker.data_source == mock_data_source


def test_last_recv_time_property(tracker: UserStreamTracker) -> None:
    assert tracker.last_recv_time == 123.456


def test_user_stream_property(tracker: UserStreamTracker) -> None:
    assert isinstance(tracker.user_stream, asyncio.Queue)


async def test_start_no_existing_task(tracker: UserStreamTracker) -> None:
    # Test normal start when no task exists
    assert tracker._user_stream_tracking_task is None

    # Mock the listen_for_user_stream to complete immediately
    async def mock_listen(*args):
        return None

    with patch.object(tracker._data_source, "listen_for_user_stream", side_effect=mock_listen):
        await tracker.start()

        assert tracker._user_stream_tracking_task is not None
        assert tracker._user_stream_tracking_task.done()


async def test_start_with_existing_done_task(tracker: UserStreamTracker) -> None:
    # Test start when existing task is done
    async def mock_coroutine():
        return "done"

    mock_existing_task = asyncio.create_task(mock_coroutine())
    await mock_existing_task  # Let it complete
    tracker._user_stream_tracking_task = mock_existing_task

    # Mock the listen_for_user_stream to complete immediately
    async def mock_listen(*args):
        return None

    with (
        patch.object(tracker._data_source, "listen_for_user_stream", side_effect=mock_listen),
        patch.object(tracker, "stop") as mock_stop,
    ):
        await tracker.start()

        mock_stop.assert_called_once()
        assert tracker._user_stream_tracking_task is not None
        assert tracker._user_stream_tracking_task.done()


async def test_start_with_existing_running_task(tracker: UserStreamTracker) -> None:
    # Return early if task is not done
    async def mock_coroutine():
        await asyncio.sleep(0.1)
        return "done"

    mock_existing_task = asyncio.create_task(mock_coroutine())
    await asyncio.sleep(0.01)  # Let task start
    tracker._user_stream_tracking_task = mock_existing_task

    with (
        patch("user_stream_tracker.tracker.safe_ensure_future") as mock_safe_ensure_future,
        patch.object(tracker, "stop") as mock_stop,
    ):
        await tracker.start()

        # Should return early without calling stop or creating new task
        mock_stop.assert_not_called()
        mock_safe_ensure_future.assert_not_called()
        assert tracker._user_stream_tracking_task == mock_existing_task


async def test_stop_no_task(tracker: UserStreamTracker) -> None:
    # Test stop when no task exists
    assert tracker._user_stream_tracking_task is None

    with patch.object(tracker._data_source, "stop") as mock_data_source_stop:
        await tracker.stop()
        mock_data_source_stop.assert_called_once()
        assert tracker._user_stream_tracking_task is None


async def test_stop_with_done_task(tracker: UserStreamTracker) -> None:
    # Test stop when task is done
    async def mock_coroutine():
        return "done"

    mock_task = asyncio.create_task(mock_coroutine())
    await mock_task  # Let it complete
    tracker._user_stream_tracking_task = mock_task

    with patch.object(tracker._data_source, "stop") as mock_data_source_stop:
        await tracker.stop()

        mock_data_source_stop.assert_called_once()
        assert tracker._user_stream_tracking_task is None


async def test_stop_with_running_task(tracker: UserStreamTracker) -> None:
    # Cancel and await running task
    async def mock_coroutine():
        await asyncio.sleep(0.1)
        return "done"

    mock_task = asyncio.create_task(mock_coroutine())
    await asyncio.sleep(0.01)  # Let task start
    tracker._user_stream_tracking_task = mock_task

    with patch.object(tracker._data_source, "stop") as mock_data_source_stop:
        await tracker.stop()

        mock_data_source_stop.assert_called_once()
        assert tracker._user_stream_tracking_task is None


async def test_stop_with_cancelled_error(tracker: UserStreamTracker) -> None:
    # Handle CancelledError when awaiting task
    async def mock_coroutine():
        raise asyncio.CancelledError()

    mock_task = asyncio.create_task(mock_coroutine())
    await asyncio.sleep(0.01)  # Let task start
    tracker._user_stream_tracking_task = mock_task

    with patch.object(tracker._data_source, "stop") as mock_data_source_stop:
        await tracker.stop()

        mock_data_source_stop.assert_called_once()
        assert tracker._user_stream_tracking_task is None
