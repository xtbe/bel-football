"""Resolution cascade tests against an in-memory team list."""

import pytest

from bel_football.exceptions import AmbiguousTeamError, TeamNotFoundError
from bel_football.models import Team
from bel_football.resolver import resolve_team


@pytest.fixture
def teams() -> list[Team]:
    return [
        Team.from_api({"team_id": 1, "name": "KAA Gent"}),
        Team.from_api({"team_id": 2, "name": "Club Brugge"}),
        Team.from_api({"team_id": 3, "name": "Cercle Brugge"}),
        Team.from_api({"team_id": 4, "name": "RSC Anderlecht"}),
    ]


def test_exact_match(teams):
    assert resolve_team("KAA Gent", teams).id == "1"


def test_prefix_stripped_match(teams):
    assert resolve_team("gent", teams).id == "1"


def test_token_match(teams):
    assert resolve_team("anderlecht", teams).id == "4"


def test_ambiguous_raises(teams):
    with pytest.raises(AmbiguousTeamError):
        resolve_team("brugge", teams)  # Club + Cercle


def test_unknown_raises(teams):
    with pytest.raises(TeamNotFoundError):
        resolve_team("charleroi", teams)
