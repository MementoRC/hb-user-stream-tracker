"""hb_compat — adapters isolating external sub-package imports for user_stream_tracker.

Contains thin wrappers so internal user_stream_tracker modules never import
external sub-packages directly, keeping the import-linter boundary clean.
"""

from user_stream_tracker.hb_compat.common import HummingbotLogger, get_logger

__all__ = ["HummingbotLogger", "get_logger"]
