"""The HTTP client. This is the *only* module that touches the network.

Config precedence for the base URL:
    explicit ``base_url=`` arg  ->  $BEL_FOOTBALL_API_BASE  ->  http://localhost:8000

The package reads ``os.environ`` directly and never calls ``load_dotenv()`` --
loading a ``.env`` file is the *application's* job, not the library's.
"""

import os

import httpx

from bel_football.exceptions import APIError
from bel_football.models import Team
from bel_football.resolver import resolve_team

ENV_BASE_URL = "BEL_FOOTBALL_API_BASE"
DEFAULT_BASE_URL = "http://localhost:8000"


class BelFootballClient:
    """Client for the local football API.

    Example:
        >>> with BelFootballClient() as client:
        ...     client.get_jupiler_pro_league_standing("gent")
    """

    def __init__(self, base_url: str | None = None, *, timeout: float = 10.0) -> None:
        resolved = base_url or os.environ.get(ENV_BASE_URL) or DEFAULT_BASE_URL
        self._client = httpx.Client(base_url=resolved.rstrip("/"), timeout=timeout)
        self._teams: list[Team] | None = None

    # --- lifecycle ---------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._client.close()

    def __enter__(self) -> "BelFootballClient":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    # --- internals -------------------------------------------------------

    def _get(self, path: str, *, params: dict | None = None) -> object:
        """GET ``path`` and return parsed JSON, or raise :class:`APIError`."""
        try:
            response = self._client.get(path, params=params)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise APIError(f"{exc.request.url} returned HTTP {exc.response.status_code}") from exc
        except httpx.RequestError as exc:
            raise APIError(f"Could not reach {exc.request.url}: {exc}") from exc
        return response.json()

    def _ensure_teams(self) -> list[Team]:
        """Return the cached team list, fetching it once on first use."""
        if self._teams is None:
            payload = self._get("/api/teams")
            self._teams = [Team.from_api(item) for item in payload]
        return self._teams

    # --- public API -----------------------------------------------------

    def refresh_teams(self) -> None:
        """Discard the cached team list so the next call re-fetches it."""
        self._teams = None

    def _resolve(self, query: str) -> Team:
        """Resolve a casual team name to a :class:`Team` (see resolver rules)."""
        return resolve_team(query, self._ensure_teams())

    def resolve_team(self, query: str) -> dict[str, str]:
        """Resolve a casual team name to ``{"id": ..., "name": ...}``.

        Raises:
            TeamNotFoundError / AmbiguousTeamError: ``query`` could not be resolved.
        """
        return self._resolve(query).to_dict()

    def get_jupiler_pro_league_standing(self, team: str, season: str | None = None) -> dict:
        """Return the Jupiler Pro League standing for ``team``.

        If ``season`` is omitted the API returns its latest available season.

        Raises:
            TeamNotFoundError / AmbiguousTeamError: ``team`` could not be resolved.
            APIError: the API request failed.
        """
        match = self._resolve(team)
        params = {"season": season} if season else None
        return self._get(f"/api/teams/{match.id}/standing", params=params)
