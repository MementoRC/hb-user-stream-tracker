"""Re-export of the hb-async-utils helpers used by user_stream_tracker.

Isolating the ``async_utils`` sub-package import here keeps the rest of
user_stream_tracker import-clean of the external dependency. Mirrors the
pattern established in hb-web-assistant's hb_compat/common.py (ADR 0001
Group D).
"""

from __future__ import annotations

from async_utils.core import safe_ensure_future, safe_gather  # type: ignore[import-untyped]

__all__ = ["safe_ensure_future", "safe_gather"]
