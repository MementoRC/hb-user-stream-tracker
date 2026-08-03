# hb-user-stream-tracker

[![CI](https://github.com/MementoRC/hb-user-stream-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/MementoRC/hb-user-stream-tracker/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/MementoRC/hb-user-stream-tracker)](https://codecov.io/gh/MementoRC/hb-user-stream-tracker)
[![PyPI version](https://badge.fury.io/py/hb-user-stream-tracker.svg)](https://badge.fury.io/py/hb-user-stream-tracker)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

User stream tracking abstractions for Hummingbot, extracted from
`hummingbot.core.data_type.user_stream_tracker` and the private user-stream-tracker
implementations duplicated across exchange connectors.

## Overview

This package will provide the private-channel (user-stream) WebSocket tracking abstractions
shared by Hummingbot exchange connectors — the account/order/balance event streams that sit
alongside the public market-data streams already covered by `hb-candles-feed` and
`hb-market-data`. It depends on `hb-web-assistant` for `WSAssistant`, the same WebSocket
connection primitive used to build authenticated private-channel listeners.

**Status: scaffold.** This repository currently contains only the project scaffolding and a
placeholder domain module (`user_stream_tracker/base.py`). The real extraction — consolidating
the ~90-96 connector-specific `*_user_stream_tracker.py` / `*_api_user_stream_data_source.py`
files scattered across `hummingbot/connector/exchange/*` — is Phase 1 Step 2 of the ADR 0001
sub-package migration and has not yet happened.

The import path `user_stream_tracker` (no `hb_` prefix) is intentional: it mirrors the
convention used by sibling packages (e.g. `web_assistant`, `market_data`) so existing
consumers can adopt it without import renaming.

## Features (planned)

- **User Stream Tracker Base**: Abstract base class for connector-specific private-channel trackers
- **WSAssistant-Based**: Built on `hb-web-assistant`'s managed WebSocket connections
- **Async-First**: Built on asyncio; all I/O is non-blocking
- **Strict Typing**: mypy strict mode throughout

## Installation

```bash
# Clone the repository
git clone https://github.com/MementoRC/hb-user-stream-tracker.git
cd hb-user-stream-tracker

# Pixi (recommended)
pixi install
pixi run test

# pip
pip install -e ".[dev]"
```

## Project Structure

```
hb-user-stream-tracker/
├── user_stream_tracker/         # Package source
│   ├── __init__.py              # Package exports
│   ├── __about__.py             # Version: "0.1.0"
│   └── base.py                  # UserStreamTrackerBase scaffold placeholder
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
├── .github/                     # CI/CD workflows
├── pyproject.toml               # Primary configuration
└── .pre-commit-config.yaml      # Pre-commit hooks
```

## Running Tests

```bash
# Pixi (recommended)
pixi run test               # All tests
pixi run test-unit          # Unit tests only
pixi run test-integration   # Integration tests only
pixi run lint               # Lint check
pixi run typecheck          # Type check
pixi run check              # Full quality + test suite

# pytest directly
pytest tests/
```

## Supersedes

This package will supersede (once Phase 1 Step 2 extraction lands):
- `hummingbot.core.data_type.user_stream_tracker` — base user-stream tracker abstraction
- Per-connector `*_user_stream_tracker.py` / `*_api_user_stream_data_source.py` implementations

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
