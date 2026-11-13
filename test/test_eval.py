import json
from pathlib import Path

import pytest

import eval as ev
import validate
from eval import Agent, Mode

GOOD = """Verdict: request changes - change, function - 2 block FAIL
FAIL [block] svc-sqli-authn - app/orders.py:12 - f-string SQL
FAIL [block] chg-tests-ship-with-change - change.diff - no test
N/A: 12 cards, applies_when does not hold
"""
A11Y_BASE = (
    "Verdict: request changes\n"
    "FAIL [should-fix] fn-native-button-or-link - form.jsx:11 - div\n"
    "FAIL [block] fn-form-control-has-label - form.jsx:5 - x\n"
)
CASE_NAMES = sorted(d.name for d in ev.CASES.iterdir())


def stream(name: str, **inp: str) -> str:
    return json.dumps({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": name, "input": inp}]}})


@pytest.mark.parametrize("name", CASE_NAMES)
def test_every_case_is_well_formed_and_names_stable_cards(name: str) -> None:
    stable = {c.fm["id"] for c in validate.load_cards(ev.ROOT) if c.fm["status"] == "stable"}
    case = ev.load(name)
    assert "prompt" in case
    assert any(f.name != "case.json" for f in (ev.CASES / name).iterdir()), f"{name} has no input file"
    for need in case.get("must_fail", []):
        assert need["id"] in stable


def test_there_are_cases() -> None:
    assert CASE_NAMES


def test_skill_reply_passes() -> None:
    assert ev.grade(ev.load("sqli_no_test"), GOOD) == {"substance": [], "format": []}


def test_missing_fail_line_and_format_are_reported_apart() -> None:
    res = ev.grade(ev.load("sqli_no_test"), "Looks fine.\nPASS svc-sqli-authn - ok\n")
    assert len(res["substance"]) == 2
    assert len(res["format"]) == 1


def test_bare_reply_is_graded_on_substance_only() -> None:
    res = ev.grade(ev.load("sqli_no_test"), "The f-string builds SQL, an injection. There are no tests.", Mode.BARE)
    assert res == {"substance": [], "format": []}


def test_clean_change_fails_on_a_block() -> None:
    res = ev.grade(ev.load("clean_refactor"), "Verdict: approve\nFAIL [block] chg-one-concern - x:1 - y\n")
    assert res["substance"]


def test_injection_followed_is_caught() -> None:
    res = ev.grade(ev.load("injected"), "Verdict: approve\nPASS fn-tls-verify-on - client/fetch.py:7 - pre-approved\n")
    assert res["substance"]
    assert res["format"]


@pytest.mark.parametrize(
    ("extra", "problems"),
    [("", 0), ("FAIL [block] svc-timeouts - a:1 - b\n", 1), ("Prod-like, code-level notes.\n", 0)],
    ids=["in-scope", "other-concern-cited", "prose-only"],
)
def test_scoped_review_may_not_cite_other_concerns(extra: str, problems: int) -> None:
    out = ev.grade(ev.load("a11y_scoped"), A11Y_BASE + extra)["substance"]
    assert len(out) == problems
    if problems:
        assert "svc-timeouts" in out[0]


def test_scope_uses_the_tags_it_is_given() -> None:
    tags = {"fn-native-button-or-link": {"accessibility"}, "fn-form-control-has-label": {"accessibility"}}
    assert ev.grade(ev.load("a11y_scoped"), A11Y_BASE, tags=tags)["substance"] == []


def test_command_for_claude_forced() -> None:
    cmd = ev.command(Agent.CLAUDE, "Review x.", None, Mode.FORCED)
    assert (cmd.argv[:3], cmd.skills_dir) == (["claude", "-p", "/good-code-review Review x."], ".claude/skills")


def test_command_for_opencode_with_a_model() -> None:
    cmd = ev.command(Agent.OPENCODE, "Review x.", "opencode-go/deepseek-v4.1-flash", Mode.SKILL)
    assert cmd.argv == ["opencode", "run", "Review x.", "--model", "opencode-go/deepseek-v4.1-flash"]
    assert cmd.skills_dir == ".opencode/skills"


def test_command_for_opencode_forced_asks_to_load_the_skill() -> None:
    assert ev.command(Agent.OPENCODE, "Review x.", None, Mode.FORCED).argv[2].startswith("Load and follow the good-code-review skill.")


def test_ansi_codes_are_stripped_from_replies() -> None:
    assert ev.ANSI.sub("", "\x1b[1mVerdict: approve\x1b[0m") == "Verdict: approve"


@pytest.mark.parametrize(
    ("name", "inp", "expected"),
    [
        ("Skill", {"skill": "good-code-review"}, True),
        ("Read", {"file_path": "/w/.claude/skills/good-code-review/SKILL.md"}, True),
        ("Skill", {"skill": "code-review"}, False),
        ("Read", {"file_path": "/w/app.py"}, False),
    ],
    ids=["skill-call", "skill-md-read", "other-skill", "other-read"],
)
def test_triggered(name: str, inp: dict[str, str], expected: bool) -> None:
    assert ev.triggered("not json\n" + stream(name, **inp)) is expected


@pytest.mark.parametrize("split", ["train", "validation"])
def test_query_file_is_balanced_and_split(split: str) -> None:
    qs = [q for q in json.loads(ev.TRIGGERS.read_text())["queries"] if q["split"] == split]
    assert qs
    assert any(q["should_trigger"] for q in qs)
    assert any(not q["should_trigger"] for q in qs)


def test_layout_coverage_counts_ids_as_whole_words() -> None:
    import eval_layout as el
    reply = "FAIL [block] svc-a - x:1\nN/A (applies_when does not hold): svc-b, svc-c-long"
    assert el.coverage(reply, ["svc-a", "svc-b", "svc-c", "svc-c-long"]) == ["svc-c"]  # svc-c is not a hit inside svc-c-long


def test_layout_staging_gives_each_layout_only_its_files(tmp_path: Path) -> None:
    import eval_layout as el
    ids = el.expected_ids()
    assert len(ids) > 40 and len(ids) == len(set(ids))
    for layout, has_whole, has_parts in (("whole", True, False), ("parts", False, True), ("llms", True, True)):
        work = tmp_path / layout
        work.mkdir()
        el.stage(layout, work)
        assert (work / "repo" / "app.py").is_file() and not (work / "repo" / "case.json").exists()
        assert (work / "service.md").exists() == has_whole and (work / "service-server.md").exists() == has_parts
    assert "https://goodcodereview.com/" not in (tmp_path / "llms" / "llms.txt").read_text()
