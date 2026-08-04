"""User stream tracking abstractions.

Ported from hummingbot.core.data_type.user_stream_tracker and
hummingbot.core.data_type.user_stream_tracker_data_source.
"""

from user_stream_tracker.__about__ import __version__
from user_stream_tracker.data_source import UserStreamTrackerDataSource
from user_stream_tracker.tracker import UserStreamTracker

__all__ = ["UserStreamTracker", "UserStreamTrackerDataSource", "__version__"]
