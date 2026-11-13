#!/usr/bin/env bash
set -euo pipefail
mkdir -p "$(dirname change.diff)"
cat > change.diff <<'EVAL_EOF'
--- a/migrations/0042_rename_email.py
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
EVAL_EOF
