"""Write the harder plugin-eval cases (evals/<case>/): planted defects that sit in less obvious cards, so a bare agent can miss them, plus a codebase coverage case.

Run `python3 tools/eval_cases_hard.py` after the codebase level gains or loses a card, because the coverage case has one grader per stable codebase card.
"""
import json
import re
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "evals"
FILE_LINE = ("evidence", r"\b[\w./-]+\.(?:py|diff|md|js|ts|go):\d+", "i")  # scored in both arms: a finding cites file:line

CASES: dict[str, dict[str, Any]] = {
    "webhook_replay": {
        "prompt": "Review handler.py before we ship it.",
        "files": {"handler.py": '''import hmac, hashlib, json, logging, os
from flask import Flask, request, abort

app = Flask(__name__)
SECRET = os.environ["WEBHOOK_SECRET"].encode()
log = logging.getLogger("hooks")


@app.post("/hooks/billing")
def billing_hook():
    body = request.get_data()
    sig = hmac.new(SECRET, body, hashlib.sha256).hexdigest()
    if sig != request.headers.get("X-Signature", ""):
        abort(401)
    event = json.loads(body)
    log.info("billing event %s for account %s", event["type"], event["account"])
    apply_event(event)
    return {"ok": True}


def apply_event(event):
    ...
'''},
        "must": [("svc-webhook-replay-window", r"replay|timestamp|tolerance|nonce|signed time"),
                 ("fn-constant-time-secret-compare", r"constant.time|compare_digest|timing"),
                 ("svc-tenant-id-in-telemetry", r"tenant")],
    },
    "list_unbounded": {
        "prompt": "Review the change in change.diff.",
        "files": {"change.diff": '''--- a/api.py
+++ b/api.py
@@ -10,6 +10,16 @@ def create_app(db):
     app = Flask(__name__)
 
+    @app.get("/orders")
+    def list_orders():
+        limit = int(request.args.get("limit", 1000000))
+        api_key = request.args["api_key"]
+        user = db.user_for_key(api_key)
+        rows = db.query("SELECT * FROM orders WHERE user_id = %s LIMIT %s", (user.id, limit))
+        return jsonify([dict(r) for r in rows])
+
     return app
'''},
        "must": [("svc-list-endpoint-paginates", r"paginat|page size|default page|cursor"),
                 ("svc-bound-client-controlled-sizes", r"cap|maximum|upper bound|unbounded|limit .*(client|user)"),
                 ("svc-no-secrets-in-url", r"query (string|param)|in the url|header")],
    },
    "migration_rename": {
        "prompt": "Review the change in change.diff.",
        "files": {"change.diff": '''--- a/migrations/0042_rename_email.py
+++ b/migrations/0042_rename_email.py
@@ -0,0 +1,8 @@
+from django.db import migrations
+
+class Migration(migrations.Migration):
+    dependencies = [("accounts", "0041_add_phone")]
+    operations = [
+        migrations.RenameField("user", "email", "contact_email"),
+    ]
--- a/accounts/views.py
+++ b/accounts/views.py
@@ -20,7 +20,7 @@ def profile(request):
-    return JsonResponse({"email": user.email})
+    return JsonResponse({"email": user.contact_email})
'''},
        "must": [("chg-expand-contract", r"expand|contract|old (column|name)|rolling|two.step|both versions|old code")],
    },
    "host_header_reset": {
        "prompt": "Review reset.py before we ship it.",
        "files": {"reset.py": '''import secrets
from flask import Flask, request

app = Flask(__name__)
TOKENS = {}


@app.post("/forgot")
def forgot():
    user = request.form["email"]
    token = secrets.token_urlsafe(16)
    TOKENS[user] = token
    link = f"https://{request.host}/reset?user={user}&token={token}"
    send_mail(user, f"Reset your password: {link}")
    return "", 204


@app.post("/reset")
def reset():
    user, token = request.form["user"], request.form["token"]
    if TOKENS.get(user) == token:
        set_password(user, request.form["password"])
        return "", 204
    return "invalid", 400


def send_mail(to, body): ...
def set_password(user, pw): ...
'''},
        "must": [("svc-host-header-trust", r"host header|allowlist|X-Forwarded|configured (base )?url|poison"),
                 ("svc-password-reset", r"single.use|reuse|expir|revoke|invalidate (the )?token|session")],
    },
}


def regex_grader(name: str, pattern: str, flags: str = "", arm: str | None = None) -> tuple[str, str]:
    fm = ["type: regex", f"pattern: {json.dumps(pattern)}"] + ([f"flags: {flags}"] if flags else []) + ([f"arm: {arm}"] if arm else [])
    return name, "---\n" + "\n".join(fm) + "\n---\n"


def write(name: str, prompt: str, files: dict[str, str], graders: list[tuple[str, str]]) -> None:
    o = OUT / name
    shutil.rmtree(o, ignore_errors=True)
    (o / "graders").mkdir(parents=True)
    (o / "prompt.md").write_text(f"---\nmax_turns: 25\nallowed_tools: [Read, Glob, Grep, Skill]\n---\n{prompt}\n")
    sh = ["#!/usr/bin/env bash", "set -euo pipefail"]
    for fname, text in files.items():
        sh += [f"mkdir -p \"$(dirname {fname})\"", f"cat > {fname} <<'EVAL_EOF'", text.rstrip("\n"), "EVAL_EOF"]
    (o / "scaffold.sh").write_text("\n".join(sh) + "\n")
    (o / "case.yaml").write_text(f'schema_version: "1.1"\nname: {name}\nplugins: ["../.."]\ncontext:\n  scaffold_script: scaffold.sh\n')
    for gname, text in graders:
        (o / "graders" / f"{gname}.md").write_text(text)
    (o / "graders" / "skill-fired.md").write_text("---\ntype: tool_used\ntool: Skill\ninput_match: '\"skill\"\\s*:\\s*\"(?:[\\w-]+:)?good-code-review\"'\n---\n")


def main() -> None:
    for name, c in CASES.items():
        gs = [regex_grader(*FILE_LINE)]
        for cid, alt in c["must"]:
            gs.append(regex_grader(f"found-{cid}", f"{re.escape(cid)}|{alt}", "i"))
            gs.append(regex_grader(f"ledger-{cid}", rf"^\s*(?:[-*]\s*)?`?FAIL\s*(?:\[[a-z-]+\])?\s*`?\s*{re.escape(cid)}\b", "m", arm="with-only"))
        gs.append(regex_grader("first-line", r"^[`*# \s]*Verdict: request changes", "", arm="with-only"))
        write(name, c["prompt"], c["files"], gs)
    # Coverage: a codebase-level review must account for every stable codebase card by id. A bare agent cannot know the ids, so this measures the skill.
    ids = sorted(card["id"] for card in json.loads((ROOT / "site/cards.json").read_text())["cards"] if card["level"] == "codebase")
    repo = {f.name: f.read_text() for f in (ROOT / "test/evals/cases/audit_repo").iterdir() if f.name != "case.json"}
    write("coverage_codebase", "Review the repo in the current directory at the codebase level only. Account for every stable card of that level.", repo,
          [regex_grader(f"covers-{i}", rf"\b{re.escape(i)}\b") for i in ids])
    print(f"wrote {len(CASES) + 1} cases; coverage case has {len(ids)} graders")


if __name__ == "__main__":
    main()
