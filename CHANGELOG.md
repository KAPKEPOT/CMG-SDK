# Changelog

All notable changes to `tonpo` are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [1.0.0] — 2026-04-10

### Added
- `TonpoClient` with `admin()` and `for_user()` factory methods
- Full account lifecycle: `create_account`, `wait_for_active`, `get_account_status`,
  `get_accounts`, `delete_account`, `pause_account`, `resume_account`
- Order placement: `place_market_buy`, `place_market_sell`, `place_limit_buy`,
  `place_limit_sell`, `place_stop_buy`, `place_stop_sell`
- Position management: `get_positions`, `close_position`, `modify_position`
- Account info: `get_account_info`
- Market data: `get_symbol_price` (REST + WebSocket cache fallback)
- WebSocket real-time data with auto-reconnection: ticks, quotes, candles,
  positions, order results, account updates
- Typed dataclass models: `TonpoConfig`, `UserCredentials`, `AccountCredentials`,
  `AccountInfo`, `Position`, `OrderResult`, `SymbolPrice`, `Tick`, `Quote`, `Candle`
- Exception hierarchy rooted at `CipherGatewayError`
- `py.typed` marker for PEP 561 IDE type-hint support
- GitHub Actions workflow for automated PyPI publishing on git tag

### Fixed
- `create_account` payload now sends camelCase keys (`mt5Login`, `mt5Password`,
  `mt5Server`) matching the gateway's `CreateAccountRequest` Rust struct
- `wait_for_active` default `timeout` raised from 60 → 180 seconds (Windows
  MT5 cold start takes 2–4 minutes on a fresh VPS)
- `wait_for_active` error message no longer shows `"None"` when `last_error`
  key exists in gateway response with a `null` value — uses `or` fallback
- Renamed `ConnectionError` → `TonpoConnectionError` to avoid shadowing
  Python's built-in `builtins.ConnectionError`
