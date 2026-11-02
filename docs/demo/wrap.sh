# Plumbing for the recording only: project-only settings, read-only tools, wrap long lines, colour the verdict tags.
claude() { command claude --setting-sources project --allowedTools "Read,Grep,Glob,Skill,Bash(git diff:*),Bash(git log:*),Bash(git show:*)" --model sonnet "$@" | fold -s -w 80 | sed -E 's/^(FAIL \[block\])/\x1b[1;31m\1\x1b[0m/; s/^(FAIL \[should-fix\])/\x1b[1;33m\1\x1b[0m/; s/^(PASS)/\x1b[1;32m\1\x1b[0m/; s/^(Verdict:)/\x1b[1m\1\x1b[0m/'; }
PS1=$'\x1b[1;36m$\x1b[0m '
cd "$(dirname "${BASH_SOURCE[0]}")/repo"
