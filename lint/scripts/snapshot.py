"""Rewrite src/goodcodereview_lint/data/cards.json from the built site/cards.json. Run `python3 tools/build.py` first."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
data = json.loads((ROOT / "site" / "cards.json").read_text())
snap = {"generated": data["generated"], "schema_version": data["schema_version"],
        "cards": {c["id"]: {k: c[k] for k in ("level", "severity", "backing", "rule", "url", "tool_gate")} for c in data["cards"]}}
out = ROOT / "lint" / "src" / "goodcodereview_lint" / "data" / "cards.json"
out.write_text(json.dumps(snap, indent=0, ensure_ascii=False) + "\n")
print(f"{len(snap['cards'])} cards, generated {snap['generated']}")
