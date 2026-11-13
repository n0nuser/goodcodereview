#!/usr/bin/env bash
set -euo pipefail
mkdir -p "$(dirname reset.py)"
cat > reset.py <<'EVAL_EOF'
import secrets
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
EVAL_EOF
