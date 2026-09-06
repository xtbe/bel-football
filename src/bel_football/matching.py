"""Pure text-normalisation helpers for matching Belgian club names.

No I/O, no state — just string in, string out. That makes them trivial to unit
test without mocking anything.
"""

import re
import unicodedata

# Prefixes/suffixes that are part of a club's *formal* name but that people
# routinely drop when typing casually ("KAA Gent" -> "gent").
KNOWN_PREFIXES: tuple[str, ...] = (
    "royale",
    "royal",
    "sporting",
    "standard de",
    "standard",
    "kaa",
    "kvc",
    "krc",
    "rsca",
    "rsc",
    "kv",
    "sk",
    "sv",
    "oh",
    "stvv",
)


def normalize(text: str) -> str:
    """Lowercase, strip accents, and collapse internal whitespace."""
    text = text.strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", text)


def strip_known_prefix(name: str) -> str:
    """Drop one leading known club prefix if present ('kaa gent' -> 'gent').

    ``name`` is expected to be already :func:`normalize`-d. Longest prefix wins,
    so 'standard de' is tried before 'standard'.
    """
    for prefix in sorted(KNOWN_PREFIXES, key=len, reverse=True):
        if name.startswith(prefix + " "):
            return name[len(prefix) :].strip()
    return name
