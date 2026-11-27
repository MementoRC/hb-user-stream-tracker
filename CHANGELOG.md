# Changelog

This file is maintained by release-please from Conventional Commits.

## 0.1.0 (2026-11-24)

### Features

* Extracted `UserStreamTracker` (`user_stream_tracker.tracker`) and `UserStreamTrackerDataSource` (`user_stream_tracker.data_source`) from hummingbot as drop-in replacements (#1)
* `hb_compat` adapters for logger, async-utils and web-assistant
* ADR 0001 L2 layer and import boundaries enforced (import-linter)

### Build

* Dependencies pinned to hb-logger v0.2.0, hb-async-utils v0.1.2, hb-web-assistant v0.1.0
* ci-framework CI, security gates, pixi.lock committed, release-please adopted (#36)
