"""The shape of cards.json, as typed models, plus the JSON Schema and a checker that are derived from them.

The dataclasses below are the only definition of the shape. `json_schema()` turns them into site/cards.schema.json,
and `check()` validates a built corpus against that schema with the standard library only.
"""
import re
from dataclasses import dataclass, field, fields, is_dataclass
from typing import Literal, Optional, Union, get_args, get_origin, get_type_hints

from validate import LACKS

SCHEMA_VERSION = 1
Status = Literal["stable", "draft"]
Severity = Literal["block", "should-fix", "discuss"]
Kind = Literal["stable", "drafts"]
Reason = Literal[*LACKS]
Level = Literal["change", "function", "module", "service", "system", "codebase", "production", "incident"]


@dataclass
class Example:
    """A code or text block from a card's FAIL or PASS section."""
    language: Optional[str]  # the fence label, such as "python" or "text"; null when the fence has none
    code: str


@dataclass
class Lacks:
    """Why a draft card is not stable yet. docs/PROMOTION.md defines each reason."""
    reason: Reason             # the main blocker, such as "orgs"
    note: str                  # one sentence on what is missing


@dataclass
class Org:
    """An organisation behind a card. tools/orgs.py maps each source URL to one."""
    id: str                    # short id, such as "w3c"
    name: str                  # display name, such as "W3C"
    sources: list[str]         # the card's URLs that this organisation publishes


@dataclass
class Card:
    id: str                    # stable identifier, such as "chg-one-concern"
    level: Level               # the review level the card belongs to
    status: Status             # only stable cards may give a verdict
    severity: Severity         # the severity of a FAIL
    concerns: list[str]        # concern tags from the closed list, such as "security"
    topics: list[str]          # the remaining tags, such as "postgres"
    lang: str                  # "core", or the pack name such as "python"
    applies_when: str
    tool_gate: Optional[str]   # a check a tool can run, or null when none exists
    note: Optional[str]        # a scope note, or null
    lacks: Optional[Lacks]     # why a draft is not stable yet; null on stable cards
    rule: str                  # the one-sentence rule
    why: str
    counterpoint: str
    fail: Example
    pass_: Example = field(metadata={"alias": "pass"})
    sources: list[str]         # URLs the rule is drawn from
    orgs: list[Org]            # every distinct organisation behind the sources, in first-cited order
    url: str                   # the card on the site
    markdown_url: str          # the level page in Markdown


@dataclass
class LevelInfo:
    id: Level
    name: str
    input: str                 # the input that routes here, such as "diff / PR"
    description: str
    stable_count: int
    draft_count: int
    gives_verdict: bool        # false when the level has no stable card
    url: str
    markdown_url: str


@dataclass
class Corpus:
    schema_version: int
    kind: Kind                 # "stable" in cards.json, "drafts" in cards-drafts.json
    name: str
    url: str
    licence: str
    generated: str             # an ISO date
    concerns: list[str]
    levels: list[LevelInfo]
    cards: list[Card]


def _key(f):
    return f.metadata.get("alias", f.name)


def to_dict(obj):
    """A model instance as plain dicts and lists, using each field's alias."""
    if is_dataclass(obj):
        return {_key(f): to_dict(getattr(obj, f.name)) for f in fields(obj)}
    if isinstance(obj, list):
        return [to_dict(x) for x in obj]
    return obj


def _schema_of(tp):
    origin = get_origin(tp)
    if is_dataclass(tp):
        return _object(tp)
    if tp is str:
        return {"type": "string"}
    if tp is int:
        return {"type": "integer"}
    if tp is bool:
        return {"type": "boolean"}
    if origin is list:
        return {"type": "array", "items": _schema_of(get_args(tp)[0])}
    if origin is Literal:
        return {"enum": list(get_args(tp))}
    if origin is Union:
        return {"anyOf": [_schema_of(a) if a is not type(None) else {"type": "null"} for a in get_args(tp)]}
    raise TypeError(f"no schema for {tp}")


def _object(cls):
    hints = get_type_hints(cls)
    props = {_key(f): _schema_of(hints[f.name]) for f in fields(cls)}
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def json_schema(base):
    """The JSON Schema (draft 2020-12) for Corpus."""
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": f"{base}/cards.schema.json",
            "title": "Good Code Review cards", **_object(Corpus)}


def check(schema, data, path="$"):
    """Return a list of problems. It understands only the keywords that json_schema() emits."""
    errs = []
    if "anyOf" in schema:
        if all(check(s, data, path) for s in schema["anyOf"]):
            errs.append(f"{path}: matches none of the allowed types")
        return errs
    if "enum" in schema:
        return [] if data in schema["enum"] else [f"{path}: {data!r} is not one of {schema['enum']}"]
    kind = {"string": str, "integer": int, "boolean": bool, "array": list, "object": dict, "null": type(None)}[schema["type"]]
    if not isinstance(data, kind) or (kind is int and isinstance(data, bool)):
        return [f"{path}: expected {schema['type']}, got {type(data).__name__}"]
    if schema["type"] == "array":
        for i, x in enumerate(data):
            errs += check(schema["items"], x, f"{path}[{i}]")
    if schema["type"] == "object":
        errs += [f"{path}: missing '{k}'" for k in schema["required"] if k not in data]
        errs += [f"{path}: unexpected '{k}'" for k in data if k not in schema["properties"]]
        for k, v in data.items():
            if k in schema["properties"]:
                errs += check(schema["properties"][k], v, f"{path}.{k}")
    return errs


def example(body, label):
    """The first fenced block after **FAIL** or **PASS** in a card body, as an Example."""
    m = re.search(rf"\*\*{label}\*\*\s*```([^\n]*)\n(.*?)\n```", body, re.S)
    return Example(m.group(1).strip() or None, m.group(2)) if m else Example(None, "")
