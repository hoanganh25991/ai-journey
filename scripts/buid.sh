#!/usr/bin/env bash
# Build docs site (notes → docs/).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/scripts/build-docs.py" "$@"
