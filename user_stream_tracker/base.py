"""Base abstraction for user (private-channel) stream trackers.

Phase 1 Step 2 scaffold placeholder. This class is intentionally minimal — it exists so
that pyproject.toml's package/coverage configuration points at real, importable code ahead
of the full connector-family extraction (~90-96 files across hummingbot/connector/exchange/*
consolidating into this package). Do not build production logic on top of this stub without
first completing that extraction and replacing this placeholder.
"""

from __future__ import annotations


class UserStreamTrackerBase:
    """Placeholder base class for connector-specific user-stream trackers.

    Extraction target: hummingbot.core.data_type.user_stream_tracker.UserStreamTracker and
    the duplicated per-connector *_user_stream_tracker.py / *_api_user_stream_data_source.py
    implementations. The real base class will define the async run loop, WSAssistant-backed
    connection lifecycle, and the message-queue contract connectors must implement.
    """

    def __init__(self) -> None:
        """Initialize the placeholder tracker (no behavior yet)."""
