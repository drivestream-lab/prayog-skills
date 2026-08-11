#!/usr/bin/env bash
# Build/refresh a repo graph into ./graphs/<repo>/ without leaving
# graphify-out/ in the app clone. Expects sibling app clones at ../<repo>.
#
# Defaults: --code-only (no API key), visualization ON (graph.html).
# Docs/labels: --with-docs / --label (needs OPENAI_* via .env — LiteLLM OK).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

export OPENAI_BASE_URL="${OPENAI_BASE_URL:-http://localhost:4000/v1}"
export OPENAI_MODEL="${OPENAI_MODEL:-llama-3.3-70b-instruct}"
export GRAPHIFY_OPENAI_MODEL="${GRAPHIFY_OPENAI_MODEL:-$OPENAI_MODEL}"

if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi

REPO="${1:-}"
BRANCH="develop"
MODE="deep"
CODE_ONLY=1
NO_VIZ=0
NO_LABEL=1

shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --branch) BRANCH="$2"; shift 2 ;;
    --update) MODE="update"; shift ;;
    --deep) MODE="deep"; shift ;;
    --code-only) CODE_ONLY=1; shift ;;
    --with-docs) CODE_ONLY=0; shift ;;
    --no-viz) NO_VIZ=1; shift ;;
    --viz) NO_VIZ=0; shift ;;
    --label) NO_LABEL=0; shift ;;
    --no-label) NO_LABEL=1; shift ;;
    *)
      if [[ "$1" == "develop" || "$1" == "main" || "$1" == "master" ]]; then
        BRANCH="$1"; shift
      elif [[ "$1" == "deep" || "$1" == "update" ]]; then
        MODE="$1"; shift
      else
        echo "Unknown arg: $1"; exit 1
      fi
      ;;
  esac
done

if [[ -z "$REPO" ]]; then
  echo "Usage: $0 <repo> [--branch develop] [--deep|--update] [--code-only|--with-docs] [--viz|--no-viz] [--label|--no-label]"
  echo "Example: $0 my-service"
  echo "Example: $0 my-service --with-docs"
  echo ""
  echo "LLM (for --with-docs / --label): OPENAI_BASE_URL=$OPENAI_BASE_URL OPENAI_MODEL=$OPENAI_MODEL"
  echo "OPENAI_API_KEY is $([[ -n "${OPENAI_API_KEY:-}" ]] && echo set || echo 'NOT set — put in .env')"
  exit 1
fi

CODE="$ROOT/../$REPO"
OUT_PARENT="$ROOT/graphs/$REPO"
OUT="$OUT_PARENT/graphify-out"

if [[ ! -d "$CODE/.git" ]]; then
  echo "ERROR: not a git repo: $CODE"
  exit 1
fi

if ! command -v graphify >/dev/null 2>&1; then
  echo "ERROR: graphify not on PATH. Install: uv tool install \"graphifyy[openai]\" --force"
  exit 1
fi

if [[ "$CODE_ONLY" -eq 0 || "$NO_LABEL" -eq 0 ]]; then
  if [[ -z "${OPENAI_API_KEY:-}" ]]; then
    echo "ERROR: OPENAI_API_KEY not set (needed for --with-docs / --label)."
    exit 1
  fi
  echo "    LLM: $OPENAI_BASE_URL  model=$OPENAI_MODEL"
fi

EXTRACT_EXTRA=()
CLUSTER_EXTRA=()
if [[ "$CODE_ONLY" -eq 1 ]]; then
  EXTRACT_EXTRA+=(--code-only)
  echo "    corpus: code-only (AST; no doc LLM)"
else
  EXTRACT_EXTRA+=(--backend openai)
  echo "    corpus: code + docs via LiteLLM/OpenAI-compatible"
fi
if [[ "$NO_VIZ" -eq 1 ]]; then
  CLUSTER_EXTRA+=(--no-viz)
else
  echo "    viz: on → graph.html"
fi
if [[ "$NO_LABEL" -eq 1 ]]; then
  CLUSTER_EXTRA+=(--no-label)
else
  CLUSTER_EXTRA+=(--backend openai)
fi

echo "==> sync $REPO @ $BRANCH"
git -C "$CODE" fetch origin
git -C "$CODE" checkout "$BRANCH"
git -C "$CODE" pull --ff-only origin "$BRANCH" 2>/dev/null || git -C "$CODE" pull --ff-only || true
SHA="$(git -C "$CODE" rev-parse HEAD)"
echo "    develop_sha=$SHA"

echo "==> graphify extract ($MODE) in $CODE"
(
  cd "$CODE"
  if [[ "$MODE" == "update" && -d graphify-out ]]; then
    graphify . --update "${EXTRACT_EXTRA[@]}"
  else
    rm -rf graphify-out
    graphify . --mode deep "${EXTRACT_EXTRA[@]}"
  fi
)

if [[ ! -f "$CODE/graphify-out/graph.json" ]]; then
  echo "ERROR: graphify did not produce graph.json"
  exit 1
fi

echo "==> graphify cluster-only (report + viz)"
(
  cd "$CODE"
  graphify cluster-only . "${CLUSTER_EXTRA[@]}"
)

mkdir -p "$OUT_PARENT"
rm -rf "$OUT"
cp -a "$CODE/graphify-out" "$OUT"
rm -rf "$CODE/graphify-out"

DIGEST="$(shasum -a 256 "$OUT/graph.json" | awk '{print $1}')"
META="$OUT_PARENT/.engg-reviews-meta.json"
cat > "$META" <<EOF
{
  "repo": "$REPO",
  "code_path": "$CODE",
  "develop_sha": "$SHA",
  "graph_digest": "sha256:$DIGEST",
  "built_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "provider": "local-graphify",
  "mode": "$MODE",
  "code_only": $([[ "$CODE_ONLY" -eq 1 ]] && echo true || echo false),
  "graph": "graphs/$REPO/graphify-out/graph.json",
  "viz": "graphs/$REPO/graphify-out/graph.html"
}
EOF

echo "==> stored $OUT"
echo "Query: graphify query \"…\" --graph $OUT/graph.json"
[[ -f "$OUT/graph.html" ]] && echo "Viz:   open \"$OUT/graph.html\""
