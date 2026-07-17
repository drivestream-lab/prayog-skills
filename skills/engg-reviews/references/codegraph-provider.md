# Codegraph provider interface

engg-reviews skills talk to a **codegraph provider**, not to Graphify by name
in protocol steps. Phase 1 default implementation is local Graphify CLI.
Phase 2 may swap in MCP + FalkorDB without rewriting skill outcomes.

## Operations

| Operation | Meaning | Phase 1 (local Graphify) | Phase 2 (shared) |
|-----------|---------|--------------------------|------------------|
| `ensure_graph(repo_path, develop_sha)` | Graph exists and matches SHA policy | `graphify <path> --mode deep --no-viz` or `graphify <path> --update` | Sync worker refresh → FalkorDB |
| `query(repo_path, question)` | BFS/context for a capability | `graphify query "<question>"` (cwd = repo) | MCP `query_graph` |
| `path(repo_path, a, b)` | Shortest path between nodes | `graphify path "A" "B"` | MCP `shortest_path` |
| `explain(repo_path, node)` | Plain-language node context | `graphify explain "Node"` | MCP `explain` / `get_node` |
| `freshness(repo_path)` | Return `develop_sha` + `graph_digest` | `git rev-parse HEAD` + sha256 of `graphify-out/graph.json` | Service metadata |

## Phase 1 install (PE laptop)

```bash
uv tool install graphifyy
# or: pipx install graphifyy
graphify --help
```

## Phase 1 fleet layout (preferred)

```text
{fleet_root}/                 # e.g. drivestream/
  {meta}/                     # PRDs — read via relative path
  {app-repos}/                # code @ develop
  pe-workspace/               # Cursor cwd for engg-reviews
    fleet.yaml
    graphs/{repo}/graphify-out/
    out/reports/
    bin/refresh-graph.sh
```

Canonical graph path: `pe-workspace/graphs/{repo}/graphify-out/graph.json`  
Code path for as-built: `../{repo}/` from pe-workspace.

Refresh helper (keeps app trees clean):

```bash
cd pe-workspace
./bin/refresh-graph.sh parichay          # deep build + copy into graphs/
./bin/refresh-graph.sh setu update       # optional third arg after branch
graphify query "org domain" --graph graphs/parichay/graphify-out/graph.json
```

Optional agent skill (review before org-wide use):

```bash
npx skills add https://github.com/safishamsi/graphify --skill graphify
```

Prefer the **CLI** (and `refresh-graph.sh`) for deterministic builds. Record
`codegraph_provider: local-graphify` either way.

## Freshness policy (Phase 1)

1. App clone must be on integration branch (default `develop`) at a known SHA.
2. Canonical graph lives under `pe-workspace/graphs/{repo}/` — not left in the
   app working tree.
3. If `graphs/{repo}/graphify-out/graph.json` is missing →
   `./bin/refresh-graph.sh {repo}` (deep).
4. If `graphs/{repo}/.engg-reviews-meta.json` `develop_sha` ≠ current app HEAD →
   re-run refresh (`update` or deep).
5. After refresh, `graph_digest = sha256(graph.json)` must match the sidecar.
6. A map row may cite graph evidence only when freshness for that repo is
   `CURRENT`. Otherwise classify delta as `unknown` or stop with `stale` /
   `blocked`.

Sidecar path: `graphs/{repo}/.engg-reviews-meta.json`

```json
{
  "develop_sha": "{sha}",
  "graph_digest": "sha256:{hex}",
  "built_at": "{ISO-8601}",
  "provider": "local-graphify",
  "mode": "deep",
  "graph": "graphs/{repo}/graphify-out/graph.json"
}
```

## Edge confidence

Graphify tags edges `EXTRACTED`, `INFERRED`, or `AMBIGUOUS`.

| Tag | Use in capability matrix | Use for product questions |
|-----|--------------------------|---------------------------|
| `EXTRACTED` | May support `exists` / `partial` / `conflict` facts | Cite as hard evidence |
| `INFERRED` | Never alone as `exists`; at best `partial` or `unknown` | Prefer as question fuel |
| `AMBIGUOUS` | Treat as `unknown` | Always question if high impact |

## Degraded mode

If the provider binary/MCP is unavailable:

- `/ensure-repo-graph` → outcome `blocked` with install steps. Do **not** PASS.
- `/prd-codebase-map` must not claim in-depth grounding. Either stop (`blocked`)
  or, only if PE explicitly authorizes degraded mode, produce
  PRD-ambiguity questions only and set
  `signals.codegraph_provider: degraded-none` and
  `signals.grounding_depth: none`.

Never equate degraded mode with Graphify-backed depth.

## Multi-repo

- Phase 1: one graph per app repo under **`pe-workspace/graphs/{repo}/`**.
- Code remains in `{fleet_root}/{repo}`; graphs are not left in app trees.
- Optional: Graphify `merge-graphs` for a fleet view — if used, still record
  per-repo SHAs/digests in the fleet table; do not hide per-repo freshness.
- Queries for a capability should use `--graph graphs/{repo}/graphify-out/graph.json`
  for the primary owning repo (impact-map / catalog), then expand to dependents.
