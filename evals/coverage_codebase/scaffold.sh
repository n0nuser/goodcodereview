#!/usr/bin/env bash
set -euo pipefail
mkdir -p "$(dirname README.md)"
cat > README.md <<'EVAL_EOF'
# reports

Run `python app.py`. Set API_KEY and AUTH_ENABLED=true in production.
EVAL_EOF
mkdir -p "$(dirname app.py)"
cat > app.py <<'EVAL_EOF'
import os

from flask import Flask, abort, request

app = Flask(__name__)
API_KEY = os.environ.get("API_KEY", "changeme")
AUTH_ENABLED = os.environ.get("AUTH_ENABLED", "false") == "true"


@app.post("/report")
def report():
    if AUTH_ENABLED and request.headers.get("X-Key") != API_KEY:
        abort(401)
    data = request.files["f"].read(1_000_000)  # a larger upload is cut at 1 MB and processed as if complete
    return {"bytes": len(data)}
EVAL_EOF
