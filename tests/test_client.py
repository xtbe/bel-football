"""HTTP-layer tests with respx mocking httpx — no running app required."""

import httpx
import pytest
import respx

from bel_football import APIError, BelFootballClient

BASE = "http://testserver"
TEAMS_JSON = [
    {"team_id": 1, "name": "KAA Gent"},
    {"team_id": 2, "name": "Club Brugge"},
]


@pytest.fixture
def client():
    with BelFootballClient(base_url=BASE) as c:
        yield c


@respx.mock
def test_team_list_is_fetched_once(client):
    route = respx.get(f"{BASE}/api/teams").mock(return_value=httpx.Response(200, json=TEAMS_JSON))
    assert client.resolve_team("gent").name == "KAA Gent"
    client.resolve_team("brugge")  # second lookup...
    assert route.call_count == 1  # ...but cache means only one HTTP call


@respx.mock
def test_get_standing_happy_path(client):
    respx.get(f"{BASE}/api/teams").mock(return_value=httpx.Response(200, json=TEAMS_JSON))
    respx.get(f"{BASE}/api/teams/1/standing").mock(
        return_value=httpx.Response(200, json={"position": 1, "points": 80})
    )
    assert client.get_jupiler_pro_league_standing("gent") == {"position": 1, "points": 80}


@respx.mock
def test_server_error_becomes_api_error(client):
    respx.get(f"{BASE}/api/teams").mock(return_value=httpx.Response(500))
    with pytest.raises(APIError):
        client.resolve_team("gent")
