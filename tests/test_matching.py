"""Pure-function tests — no mocks, no fixtures needed."""

import pytest

from bel_football.matching import normalize, strip_known_prefix


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("RSC Anderlecht", "rsc anderlecht"),
        ("  Club   Brugge  ", "club brugge"),
        ("Standard Liège", "standard liege"),  # accents stripped
        ("KAA GENT", "kaa gent"),
    ],
)
def test_normalize(raw, expected):
    assert normalize(raw) == expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("kaa gent", "gent"),
        ("standard de liege", "liege"),  # longest prefix ("standard de") wins
        ("club brugge", "club brugge"),  # "club" is not a known prefix
        ("rsca", "rsca"),  # prefix with no trailing token -> unchanged
    ],
)
def test_strip_known_prefix(name, expected):
    assert strip_known_prefix(name) == expected
