"""Exception hierarchy for bel_football.

Everything the package raises inherits from :class:`BelFootballError`, so callers
can catch that one class. The leaf types also inherit from a stdlib exception
(``ValueError`` / ``RuntimeError``) so existing ``except ValueError`` code from the
original script keeps working.
"""


class BelFootballError(Exception):
    """Base class for every error raised by bel_football."""


class TeamNotFoundError(BelFootballError, ValueError):
    """No team matched the given query."""


class AmbiguousTeamError(BelFootballError, ValueError):
    """The query matched more than one team; be more specific."""


class APIError(BelFootballError, RuntimeError):
    """The football API returned an error status or could not be reached."""
