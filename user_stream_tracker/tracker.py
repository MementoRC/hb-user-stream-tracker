"""User stream tracker.

Extracted from ``hummingbot.core.data_type.user_stream_tracker``.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
from typing import TYPE_CHECKING, Any

from user_stream_tracker.hb_compat import safe_ensure_future, safe_gather

if TYPE_CHECKING:
    from user_stream_tracker.data_source import UserStreamTrackerDataSource
    from user_stream_tracker.hb_compat import HummingbotLogger


class UserStreamTracker:
    _ust_logger: HummingbotLogger | None = None

    @classmethod
    def logger(cls) -> HummingbotLogger:
        if cls._ust_logger is None:
            cls._ust_logger = logging.getLogger(__name__)
        return cls._ust_logger

    def __init__(self, data_source: UserStreamTrackerDataSource) -> None:
        self._user_stream: asyncio.Queue[Any] = asyncio.Queue()
        self._data_source = data_source
        self._user_stream_tracking_task: asyncio.Task[None] | None = None

    @property
    def data_source(self) -> UserStreamTrackerDataSource:
        return self._data_source

    @property
    def last_recv_time(self) -> float:
        return self.data_source.last_recv_time

    async def start(self) -> None:
        # Prevent concurrent start() calls
        if (
            self._user_stream_tracking_task is not None
            and not self._user_stream_tracking_task.done()
        ):
            return

        # Stop any existing task
        await self.stop()

        self._user_stream_tracking_task = safe_ensure_future(
            self.data_source.listen_for_user_stream(self._user_stream)
        )
        await safe_gather(self._user_stream_tracking_task)

    async def stop(self) -> None:
        """Stop the user stream tracking task and clean up resources."""
        if (
            self._user_stream_tracking_task is not None
            and not self._user_stream_tracking_task.done()
        ):
            self._user_stream_tracking_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._user_stream_tracking_task

        await self._data_source.stop()

        self._user_stream_tracking_task = None

    @property
    def user_stream(self) -> asyncio.Queue[Any]:
        return self._user_stream
