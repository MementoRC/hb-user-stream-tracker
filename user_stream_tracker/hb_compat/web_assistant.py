"""Re-export of the hb-web-assistant WSAssistant used by user_stream_tracker.

Isolating the ``web_assistant`` sub-package import here keeps the rest of
user_stream_tracker import-clean of the external dependency. Mirrors the
pattern established in hb-web-assistant's hb_compat/common.py (ADR 0001
Group D).
"""

from __future__ import annotations

from web_assistant.ws_assistant import WSAssistant  # type: ignore[import-untyped]

__all__ = ["WSAssistant"]
