#!/usr/bin/env bash
# Build + serve docs under /ai-lab (GitHub Pages–like review).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/scripts/serve-docs.py" "$@"
