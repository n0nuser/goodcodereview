#!/usr/bin/env bash
set -euo pipefail
mkdir -p "$(dirname change.diff)"
cat > change.diff <<'EVAL_EOF'
--- a/api.py
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
EVAL_EOF
