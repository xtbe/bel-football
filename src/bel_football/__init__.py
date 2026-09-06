"""bel_football -- a small client for a local football API.

Jupiler Pro League standings and fuzzy Belgian club-name resolution.
"""

from importlib.metadata import PackageNotFoundError, version

from bel_football.client import BelFootballClient
from bel_football.exceptions import (
    AmbiguousTeamError,
    APIError,
    BelFootballError,
    TeamNotFoundError,
)
from bel_football.models import Team

try:
    __version__ = version("bel-football")
except PackageNotFoundError:  # pragma: no cover - only when running from a raw checkout
    __version__ = "0.0.0.dev0"

__all__ = [
    "BelFootballClient",
    "Team",
    "BelFootballError",
    "TeamNotFoundError",
    "AmbiguousTeamError",
    "APIError",
    "__version__",
]
