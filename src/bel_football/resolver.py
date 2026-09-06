"""Pure team-name resolution: a query string + a list of teams -> one Team.

Lifted from the original ``resolve_team_id``, with the network fetch removed.
The client passes in the team list it already has cached.
"""

from bel_football.exceptions import AmbiguousTeamError, TeamNotFoundError
from bel_football.matching import normalize
from bel_football.models import Team


def resolve_team(query: str, teams: list[Team]) -> Team:
    """Resolve a casual team name to exactly one :class:`Team`.

    Tries, in order: exact normalised match, prefix-stripped exact match,
    token-subset match, then substring match. The first stage that yields a
    single hit wins.

    Raises:
        TeamNotFoundError: nothing matched.
        AmbiguousTeamError: a stage matched more than one team.
    """
    q = normalize(query)
    q_tokens = set(q.split())

    exact = [t for t in teams if t.full_norm == q]
    if len(exact) == 1:
        return exact[0]

    stripped_exact = [t for t in teams if t.stripped_norm == q]
    if len(stripped_exact) == 1:
        return stripped_exact[0]

    token_match = [t for t in teams if q_tokens and q_tokens.issubset(t.tokens)]
    if len(token_match) == 1:
        return token_match[0]
    if len(token_match) > 1:
        raise AmbiguousTeamError(_ambiguous_message(query, token_match))

    substring_match = [t for t in teams if q in t.stripped_norm]
    if len(substring_match) == 1:
        return substring_match[0]
    if len(substring_match) > 1:
        raise AmbiguousTeamError(_ambiguous_message(query, substring_match))

    raise TeamNotFoundError(f'No team found matching "{query}"')


def _ambiguous_message(query: str, matches: list[Team]) -> str:
    names = ", ".join(t.name for t in matches)
    return f'Multiple teams match "{query}": {names}'
