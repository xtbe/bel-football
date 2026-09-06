"""Data models returned by the client."""

from dataclasses import dataclass, field

from bel_football.matching import normalize, strip_known_prefix


@dataclass(frozen=True)
class Team:
    """A football team as returned by the API, plus cached match keys.

    Immutable and hashable. The derived fields (``full_norm`` etc.) are computed
    once in :meth:`from_api` and used by the resolver; they're hidden from
    ``repr`` to keep debugging output clean.
    """

    id: str
    name: str
    full_norm: str = field(repr=False)
    stripped_norm: str = field(repr=False)
    tokens: frozenset[str] = field(repr=False)

    @classmethod
    def from_api(cls, payload: dict) -> "Team":
        """Build a :class:`Team` from one raw ``/api/teams`` JSON object."""
        full_norm = normalize(payload["name"])
        return cls(
            id=str(payload["team_id"]),
            name=payload["name"],
            full_norm=full_norm,
            stripped_norm=strip_known_prefix(full_norm),
            tokens=frozenset(full_norm.split()),
        )

    def to_dict(self) -> dict[str, str]:
        """Return the public fields as a plain JSON-serialisable dict."""
        return {"id": self.id, "name": self.name}
