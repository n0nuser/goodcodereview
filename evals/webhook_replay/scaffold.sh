#!/usr/bin/env bash
set -euo pipefail
mkdir -p "$(dirname handler.py)"
cat > handler.py <<'EVAL_EOF'
import hmac, hashlib, json, logging, os
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
EVAL_EOF
