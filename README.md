# bel-football

Python client for a **local football API** — Jupiler Pro League standings, with
fuzzy resolution of casual Belgian club names ("gent" → *KAA Gent*).

## Install

From GitHub (no PyPI release):

```bash
pip install "git+https://github.com/xtbe/bel-football.git"
# pin a release:
pip install "git+https://github.com/xtbe/bel-football.git@v0.1.0"
```

With uv, in another project:

```bash
uv add "git+https://github.com/xtbe/bel-football.git@v0.1.0"
```

## Configure

The client needs the base URL of your local football API. Resolution order:

1. `base_url=` argument to `BelFootballClient(...)`
2. `BEL_FOOTBALL_API_BASE` environment variable
3. `http://localhost:8000` (default)

The package reads the environment variable directly. It does **not** load `.env`
files — that is your application's job (e.g. call `dotenv.load_dotenv()` yourself
before constructing the client).

## Quick start

```python
from bel_football import BelFootballClient

with BelFootballClient() as client:
    team = client.resolve_team("kaa gent")
    print(team)                      # {'id': '1', 'name': 'KAA Gent'}

    standing = client.get_jupiler_pro_league_standing("gent")
    print(standing)

    # a specific season:
    client.get_jupiler_pro_league_standing("club brugge", season="2024-2025")
```

## Team name matching

`resolve_team` and `get_jupiler_pro_league_standing` accept casual names. Matching
tries, in order: exact match → known-prefix stripped (`KAA`, `RSC`, `Standard de`,
…) → all query words present → substring. The first stage with a single hit wins.

```python
client.resolve_team("gent")           # KAA Gent      (prefix stripped)
client.resolve_team("anderlecht")     # RSC Anderlecht
client.resolve_team("brugge")         # AmbiguousTeamError: Club + Cercle
client.resolve_team("charleroi?!")    # TeamNotFoundError
```

## Errors

All exceptions inherit from `BelFootballError`:

| Exception | Also a | Raised when |
|---|---|---|
| `TeamNotFoundError` | `ValueError` | no team matched the query |
| `AmbiguousTeamError` | `ValueError` | more than one team matched |
| `APIError` | `RuntimeError` | the API returned an error status or was unreachable |

```python
from bel_football import BelFootballClient, BelFootballError

try:
    with BelFootballClient() as client:
        client.get_jupiler_pro_league_standing("gent")
except BelFootballError as exc:
    print(f"lookup failed: {exc}")
```

## Development

```bash
uv sync                    # create .venv, install deps + dev tools
uv run pytest              # run the test suite
uv run ruff check .        # lint
uv run ruff format .       # format
uv build                   # build sdist + wheel into dist/
```

See [docs/usage.md](docs/usage.md) for the full guide.

## License

MIT — see [LICENSE](LICENSE).
