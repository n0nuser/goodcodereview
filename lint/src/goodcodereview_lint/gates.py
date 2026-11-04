"""The map from linter rule codes to cards, and the snapshot of the cards it points at."""
import csv
import json
from dataclasses import dataclass
from importlib import resources
from typing import Any


@dataclass(frozen=True)
class Gate:
    """One linter rule that a card names as its gate."""

    tool: str
    code: str
    card: str
    scope: str  # "full": the rule is the card's whole check. "partial": it catches part of what the card asks for.


def _data(name: str) -> str:
    return resources.files("goodcodereview_lint").joinpath("data", name).read_text(encoding="utf-8")


def load_gates() -> list[Gate]:
    return [Gate(r["tool"], r["code"], r["card"], r["scope"]) for r in csv.DictReader(_data("gates.tsv").splitlines(), delimiter="\t")]


def load_snapshot() -> dict[str, Any]:
    """The cards as they were when this release was built: id -> level, severity, backing, rule, url, tool_gate."""
    data: dict[str, Any] = json.loads(_data("cards.json"))
    return data


def by_code(gates: list[Gate], tool: str = "ruff") -> dict[str, list[Gate]]:
    """Gates of one tool keyed by rule code. A code can serve more than one card; the card where the rule is the whole check comes first."""
    out: dict[str, list[Gate]] = {}
    for g in sorted((g for g in gates if g.tool == tool), key=lambda g: g.scope != "full"):
        out.setdefault(g.code, []).append(g)
    return out
