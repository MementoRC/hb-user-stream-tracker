"""hb_compat — adapters isolating external sub-package imports for user_stream_tracker.

Contains thin wrappers so internal user_stream_tracker modules never import
external sub-packages directly, keeping the import-linter boundary clean.
"""

from user_stream_tracker.hb_compat.async_utils import safe_ensure_future, safe_gather
from user_stream_tracker.hb_compat.common import HummingbotLogger, get_logger
from user_stream_tracker.hb_compat.web_assistant import WSAssistant

__all__ = [
    "HummingbotLogger",
    "WSAssistant",
    "get_logger",
    "safe_ensure_future",
    "safe_gather",
]
