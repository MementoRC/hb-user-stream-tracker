"""Tests for user_stream_tracker.hb_compat — the external sub-package import
boundary. Covers the re-export surface and the ``get_logger`` helper.
"""

import logging

from async_utils.core import safe_ensure_future as _safe_ensure_future
from async_utils.core import safe_gather as _safe_gather
from logger import HummingbotLogger as _HummingbotLogger
from web_assistant.ws_assistant import WSAssistant as _WSAssistant

from user_stream_tracker import hb_compat
from user_stream_tracker.hb_compat import (
    HummingbotLogger,
    WSAssistant,
    get_logger,
    safe_ensure_future,
    safe_gather,
)
from user_stream_tracker.hb_compat.common import get_logger as common_get_logger


def test_get_logger_returns_named_logger() -> None:
    logger = get_logger("user_stream_tracker.test_hb_compat")
    assert isinstance(logger, logging.Logger)
    assert logger is logging.getLogger("user_stream_tracker.test_hb_compat")


def test_get_logger_is_the_common_module_implementation() -> None:
    assert get_logger is common_get_logger


def test_all_exports_are_present_on_the_package() -> None:
    for name in hb_compat.__all__:
        assert hasattr(hb_compat, name)


def test_reexported_names_are_the_underlying_symbols() -> None:
    assert safe_ensure_future is _safe_ensure_future
    assert safe_gather is _safe_gather
    assert HummingbotLogger is _HummingbotLogger
    assert WSAssistant is _WSAssistant
