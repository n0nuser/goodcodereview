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
