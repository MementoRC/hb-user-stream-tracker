"""Tests for user_stream_tracker.data_source — ported from hummingbot's
test_user_stream_tracker_data_source.py, rewritten to pytest-native style
(no unittest).
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from web_assistant.ws_assistant import WSAssistant

from user_stream_tracker.data_source import UserStreamTrackerDataSource


class MockUserStreamTrackerDataSource(UserStreamTrackerDataSource):
    """Mock implementation for testing"""

    def __init__(self) -> None:
        super().__init__()
        self._manage_listen_key_task = None
        self._current_listen_key = None
        self._listen_key_initialized_event = asyncio.Event()

    async def _connected_websocket_assistant(self) -> WSAssistant:
        return AsyncMock(spec=WSAssistant)

    async def _subscribe_channels(self, websocket_assistant: WSAssistant):
        pass


class BareUserStreamTrackerDataSource(UserStreamTrackerDataSource):
    """Minimal implementation without listen-key bookkeeping attributes."""

    async def _connected_websocket_assistant(self) -> WSAssistant:
        return AsyncMock(spec=WSAssistant)

    async def _subscribe_channels(self, websocket_assistant: WSAssistant):
        pass


@pytest.fixture
def data_source() -> MockUserStreamTrackerDataSource:
    return MockUserStreamTrackerDataSource()


def test_init(data_source: MockUserStreamTrackerDataSource) -> None:
    assert data_source._ws_assistant is None


def test_logger_creation(data_source: MockUserStreamTrackerDataSource) -> None:
    logger = data_source.logger()
    assert logger is not None
    assert logger == data_source._logger


def test_last_recv_time_no_ws_assistant(data_source: MockUserStreamTrackerDataSource) -> None:
    assert data_source.last_recv_time == 0


def test_last_recv_time_with_ws_assistant(data_source: MockUserStreamTrackerDataSource) -> None:
    mock_ws = MagicMock()
    mock_ws.last_recv_time = 123.456
    data_source._ws_assistant = mock_ws
    assert data_source.last_recv_time == 123.456


@patch("asyncio.sleep")
async def test_sleep(mock_sleep, data_source: MockUserStreamTrackerDataSource) -> None:
    await data_source._sleep(1.5)
    mock_sleep.assert_called_once_with(1.5)


def test_time(data_source: MockUserStreamTrackerDataSource) -> None:
    with patch("time.time", return_value=123.456):
        assert data_source._time() == 123.456


async def test_process_event_message_empty(data_source: MockUserStreamTrackerDataSource) -> None:
    queue = asyncio.Queue()
    await data_source._process_event_message({}, queue)
    assert queue.empty()


async def test_process_event_message_non_empty(
    data_source: MockUserStreamTrackerDataSource,
) -> None:
    queue = asyncio.Queue()
    message = {"test": "data"}
    await data_source._process_event_message(message, queue)
    assert not queue.empty()
    result = queue.get_nowait()
    assert result == message


async def test_on_user_stream_interruption_no_ws_assistant(
    data_source: MockUserStreamTrackerDataSource,
) -> None:
    await data_source._on_user_stream_interruption(None)


async def test_on_user_stream_interruption_with_ws_assistant(
    data_source: MockUserStreamTrackerDataSource,
) -> None:
    mock_ws = AsyncMock()
    await data_source._on_user_stream_interruption(mock_ws)
    mock_ws.disconnect.assert_called_once()


async def test_send_ping(data_source: MockUserStreamTrackerDataSource) -> None:
    mock_ws = AsyncMock()
    await data_source._send_ping(mock_ws)
    mock_ws.ping.assert_called_once()


async def test_stop_with_manage_listen_key_task_not_done(
    data_source: MockUserStreamTrackerDataSource,
) -> None:
    # Cancel and await _manage_listen_key_task when not done
    async def mock_coroutine():
        await asyncio.sleep(0.1)
        return "done"

    mock_task = asyncio.create_task(mock_coroutine())
    await asyncio.sleep(0.01)  # Let task start
    data_source._manage_listen_key_task = mock_task

    await data_source.stop()

    assert data_source._manage_listen_key_task is None


async def test_stop_with_manage_listen_key_task_done(
    data_source: MockUserStreamTrackerDataSource,
) -> None:
    # Done tasks are not cancelled
    async def mock_coroutine():
        return "done"

    mock_task = asyncio.create_task(mock_coroutine())
    await mock_task  # Let it complete
    data_source._manage_listen_key_task = mock_task

    await data_source.stop()

    assert data_source._manage_listen_key_task is None


async def test_stop_with_manage_listen_key_task_cancelled_error(
    data_source: MockUserStreamTrackerDataSource,
) -> None:
    # Handle CancelledError when awaiting task
    async def mock_coroutine():
        raise asyncio.CancelledError()

    mock_task = asyncio.create_task(mock_coroutine())
    # Wait a bit to let task start
    await asyncio.sleep(0.01)
    data_source._manage_listen_key_task = mock_task

    await data_source.stop()

    assert data_source._manage_listen_key_task is None


async def test_stop_clears_listen_key_state(data_source: MockUserStreamTrackerDataSource) -> None:
    # Clear listen key state
    data_source._current_listen_key = "test_key"
    data_source._listen_key_initialized_event = asyncio.Event()
    data_source._listen_key_initialized_event.set()

    await data_source.stop()

    assert data_source._current_listen_key is None
    assert not data_source._listen_key_initialized_event.is_set()


async def test_stop_disconnects_ws_assistant(data_source: MockUserStreamTrackerDataSource) -> None:
    # Disconnect and clear ws_assistant
    mock_ws = AsyncMock()
    data_source._ws_assistant = mock_ws

    await data_source.stop()

    mock_ws.disconnect.assert_called_once()
    assert data_source._ws_assistant is None


async def test_stop_no_ws_assistant(data_source: MockUserStreamTrackerDataSource) -> None:
    # stop works when no ws_assistant exists
    data_source._ws_assistant = None

    await data_source.stop()

    assert data_source._ws_assistant is None


async def test_stop_skips_missing_listen_key_attributes() -> None:
    # hasattr(...) branches take the "attribute absent" path when a subclass
    # never sets up listen-key bookkeeping
    bare = BareUserStreamTrackerDataSource()

    await bare.stop()

    assert bare._ws_assistant is None
    assert not hasattr(bare, "_current_listen_key")
    assert not hasattr(bare, "_listen_key_initialized_event")


def test_logger_creation_reuses_cached_logger(
    data_source: MockUserStreamTrackerDataSource,
) -> None:
    first = data_source.logger()
    second = data_source.logger()
    assert first is second


async def test_process_websocket_messages_forwards_events(
    data_source: MockUserStreamTrackerDataSource,
) -> None:
    class _Message:
        def __init__(self, data: dict) -> None:
            self.data = data

    async def _iter_messages():
        for payload in ({"a": 1}, {"b": 2}):
            yield _Message(payload)

    mock_ws = MagicMock()
    mock_ws.iter_messages = _iter_messages
    queue: asyncio.Queue = asyncio.Queue()

    await data_source._process_websocket_messages(websocket_assistant=mock_ws, queue=queue)

    assert queue.qsize() == 2
    assert queue.get_nowait() == {"a": 1}
    assert queue.get_nowait() == {"b": 2}


async def test_listen_for_user_stream_happy_path_propagates_cancelled(
    data_source: MockUserStreamTrackerDataSource,
) -> None:
    mock_ws = AsyncMock(spec=WSAssistant)
    queue: asyncio.Queue = asyncio.Queue()

    with (
        patch.object(
            data_source, "_connected_websocket_assistant", AsyncMock(return_value=mock_ws)
        ) as mock_connect,
        patch.object(data_source, "_subscribe_channels", AsyncMock()) as mock_subscribe,
        patch.object(data_source, "_send_ping", AsyncMock()) as mock_ping,
        patch.object(
            data_source,
            "_process_websocket_messages",
            AsyncMock(side_effect=asyncio.CancelledError()),
        ) as mock_process,
        patch.object(data_source, "_on_user_stream_interruption", AsyncMock()) as mock_interrupt,
        pytest.raises(asyncio.CancelledError),
    ):
        await data_source.listen_for_user_stream(queue)

    mock_connect.assert_called_once()
    mock_subscribe.assert_called_once_with(websocket_assistant=mock_ws)
    mock_ping.assert_called_once_with(websocket_assistant=mock_ws)
    mock_process.assert_called_once_with(websocket_assistant=mock_ws, queue=queue)
    mock_interrupt.assert_called_once_with(websocket_assistant=mock_ws)
    assert data_source._ws_assistant is None


async def test_listen_for_user_stream_connection_error_warns_and_retries(
    data_source: MockUserStreamTrackerDataSource,
) -> None:
    queue: asyncio.Queue = asyncio.Queue()
    connection_exception = ConnectionError("closed")

    with (
        patch.object(
            data_source,
            "_connected_websocket_assistant",
            AsyncMock(side_effect=[connection_exception, asyncio.CancelledError()]),
        ) as mock_connect,
        patch.object(data_source, "_on_user_stream_interruption", AsyncMock()) as mock_interrupt,
        patch.object(data_source.logger(), "warning") as mock_warning,
        pytest.raises(asyncio.CancelledError),
    ):
        await data_source.listen_for_user_stream(queue)

    assert mock_connect.call_count == 2
    mock_warning.assert_called_once()
    assert mock_interrupt.call_count == 2
    assert data_source._ws_assistant is None


async def test_listen_for_user_stream_generic_exception_sleeps_and_propagates_cancelled(
    data_source: MockUserStreamTrackerDataSource,
) -> None:
    queue: asyncio.Queue = asyncio.Queue()
    boom = RuntimeError("boom")

    with (
        patch.object(data_source, "_connected_websocket_assistant", AsyncMock(side_effect=boom)),
        patch.object(
            data_source, "_sleep", AsyncMock(side_effect=asyncio.CancelledError())
        ) as mock_sleep,
        patch.object(data_source, "_on_user_stream_interruption", AsyncMock()) as mock_interrupt,
        patch.object(data_source.logger(), "exception") as mock_exception,
        pytest.raises(asyncio.CancelledError),
    ):
        await data_source.listen_for_user_stream(queue)

    mock_exception.assert_called_once()
    mock_sleep.assert_called_once_with(1.0)
    mock_interrupt.assert_called_once()
    assert data_source._ws_assistant is None
