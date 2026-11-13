#!/usr/bin/env bash
set -euo pipefail
cat > README.md <<'EVAL_EOF'
# tidy

A command-line tool. `python cli.py FILE [--yes]`.
EVAL_EOF
cat > cli.py <<'EVAL_EOF'
import argparse
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument("path")
    p.add_argument("--yes", action="store_true")
    a = p.parse_args()
    try:
        data = open(a.path).read()
    except OSError as e:
        print(f"error: {e}")  # an error on stdout, and the process exits 0
        return 0
    if not a.yes and input("Delete the file? [y/N] ").lower() != "y":
        return 0
    print(len(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
EVAL_EOF
