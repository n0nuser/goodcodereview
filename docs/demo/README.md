# Demo clip

`demo.gif` is a real run, not a replay. `claude -p` (Sonnet) reviewed the Redis caching PR of [fastapi-archetype](https://github.com/n0nuser/fastapi-archetype) (commit `45cbae2` against its parent) with only the `good-code-review` skill installed. The agent's wait of about 50 seconds is sped up tenfold and says so on screen.

`wrap.sh` holds the recording plumbing: project-only settings, read-only tools, line wrapping at 80 columns, and colour for the `FAIL`, `PASS`, and `Verdict:` tags. `review.tape` is the [VHS](https://github.com/charmbracelet/vhs) script. The review differs from run to run, so a rerun finds a different set of issues.
