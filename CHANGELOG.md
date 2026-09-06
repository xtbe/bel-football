# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-09-06

### Changed
- `BelFootballClient.resolve_team()` now returns a plain `{"id", "name"}` dict
  instead of a `Team` object, for consistency with
  `get_jupiler_pro_league_standing()` and easier use as an agent tool.

### Added
- `Team.to_dict()` for JSON-serialisable output.

## [0.1.0] - 2026-09-06

### Added
- `BelFootballClient` with `resolve_team`, `get_jupiler_pro_league_standing`,
  `refresh_teams`, and context-manager support.
- Fuzzy Belgian club-name resolution (`bel_football.resolver`,
  `bel_football.matching`), ported from the original standalone script.
- `Team` dataclass model.
- `BelFootballError` exception hierarchy: `TeamNotFoundError`,
  `AmbiguousTeamError`, `APIError`.
- Base-URL configuration via constructor argument, the
  `BEL_FOOTBALL_API_BASE` environment variable, or the
  `http://localhost:8000` default.
- Test suite (pytest + respx) and ruff lint/format configuration.

[Unreleased]: https://github.com/xtbe/bel-football/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/xtbe/bel-football/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/xtbe/bel-football/releases/tag/v0.1.0
