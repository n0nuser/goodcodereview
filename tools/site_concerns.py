"""Static Markdown lists for one concern or one level: the text the Worker returns for /concerns.md?concern=<c> or ?level=<l>.

The Worker (src/worker.js, `markdown()`) renders the same text for every other filter. Python cannot call it, so this module renders the
two single-filter cases and test/worker.test.mjs asserts that each file equals the Worker's output byte for byte.
"""
from typing import Any

FILTER_NOTE = "A card matches when it lists any value given for each filter."
VERDICT_LINE = ("Report each check as `PASS`, `FAIL`, or `N/A` with `file:line` evidence. A `FAIL` carries the card's severity. "
                "Any `block` `FAIL` means request changes.")


def card_line(card: dict[str, Any]) -> str:
    return f"- [`{card['id']}`]({card['url']}) [{card['severity']}] {{{', '.join(card['concerns'])}}}: {card['rule']}"


def markdown(index: dict[str, Any], key: str, value: str) -> str:
    """The list of stable cards whose `concern` (key "concern") or `level` (key "level") is `value`, from the slim index data."""
    cards = [c for c in index["cards"] if (value in c["concerns"] if key == "concern" else c["level"] == value)]
    lines = ["# Concerns", "", f"Stable cards that match {key}: {value}. {FILTER_NOTE}", f"{len(cards)} of {len(index['cards'])} cards.",
             "", VERDICT_LINE, "", *[card_line(c) for c in cards]]
    return "\n".join(lines) + "\n"


def files(index: dict[str, Any]) -> dict[str, str]:
    """concerns/<concern>.md for each concern with cards, and concerns/level-<level>.md for each level with cards."""
    out = {}
    for concern in index["concerns"]:
        if any(concern in c["concerns"] for c in index["cards"]):
            out[f"concerns/{concern}.md"] = markdown(index, "concern", concern)
    for level in index["levels"]:
        if any(c["level"] == level for c in index["cards"]):
            out[f"concerns/level-{level}.md"] = markdown(index, "level", level)
    return out
