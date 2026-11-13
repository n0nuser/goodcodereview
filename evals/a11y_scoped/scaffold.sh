#!/usr/bin/env bash
set -euo pipefail
cat > form.jsx <<'EVAL_EOF'
export function Signup({ onSubmit }) {
  const [email, setEmail] = useState("");
  return (
    <form onSubmit={onSubmit}>
      <input
        type="email"
        placeholder="Email address"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <div className="btn" onClick={onSubmit}>
        Sign up
      </div>
    </form>
  );
}
EVAL_EOF
