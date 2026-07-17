#!/usr/bin/env bash
# Thin wrapper: download is optional; prefers sibling install_engg_reviews.py.
# Usage:
#   ./scripts/install-engg-reviews.sh --target /path/to/pe-workspace [--ref pe-rc-2]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PY="${ROOT}/install_engg_reviews.py"
if [[ ! -f "$PY" ]]; then
  echo "Missing $PY" >&2
  exit 1
fi
exec python3 "$PY" "$@"
