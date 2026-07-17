# Layout defaults — engg-reviews (pe-workspace + fleet siblings)

## Preferred cwd (Phase 1)

Open **`{fleet_root}/pe-workspace/`** (parallel to app repos and meta).
Do **not** require meta as the Cursor project.

```text
{fleet_root}/                    e.g. …/handson/drivestream
  drivestream-meta/              # or {client}-meta — PRDs / Meta PRs
  parichay/, setu/, …            # app clones @ develop
  pe-workspace/                  # ← engg-reviews cwd
    fleet.yaml
    graphs/{repo}/graphify-out/  # canonical graphs (not left in app trees)
    out/reports/                 # PE map / resolution drafts
    bin/refresh-graph.sh
    .agents/skills/              # symlinks to prayog-skills engg-reviews
```

Resolve paths from `fleet.yaml` when present; else these defaults.

## pe-workspace keys

| Key | Default |
|-----|---------|
| `fleet_root` | `..` (parent of pe-workspace) |
| `meta_path` | `../drivestream-meta` or `../{client}-meta` |
| `graphs_dir` | `graphs/` |
| `graph_json` | `graphs/{repo}/graphify-out/graph.json` |
| `graph_meta` | `graphs/{repo}/.engg-reviews-meta.json` |
| `reports_dir` | `out/reports/` |
| map artifact | `{reports_dir}/PRD-Codebase-Map-{INIT}.md` |
| fleet status | `{reports_dir}/Graph-Fleet-Status-{INIT}.md` |
| question resolution | `{reports_dir}/Product-Question-Resolution-{INIT}.md` |
| `integration_branch` | `develop` |

## Meta (read; optional write-back)

| Key | Default under `meta_path` |
|-----|---------------------------|
| `prd_root` | `{meta_path}/prd/` |
| `meta_reports_dir` | `{meta_path}/prd/reports/` |
| `service_catalog` | `{meta_path}/config/service-catalog.yaml` |

Phase 1 default: write maps under **pe-workspace `out/reports/`**. Promote into
meta `prd/reports/` only when PE explicitly chooses (still no gate labels).

## App siblings (code + as-built)

| Key | Default |
|-----|---------|
| `code_path` | `{fleet_root}/{repo}/` |
| `constitution` | `AGENTS.md` |
| `as_built` | `docs/specification/as-built/implementation-status.md` |
| `adr_dir` | `docs/specification/adr` |
| `spec_root` | `docs/specification` |

If `.harness/profile.yaml` exists in an app clone, prefer its `layout.*` for
as-built / adr paths.

## Graph refresh

Prefer `pe-workspace/bin/refresh-graph.sh {repo}`:

1. Sync `{code_path}` @ develop  
2. Run Graphify in the app clone  
3. Copy `graphify-out/` → `graphs/{repo}/graphify-out/`  
4. Remove `graphify-out/` from the app clone  
5. Write `.engg-reviews-meta.json` (sha + digest)

Queries:

```bash
graphify query "…" --graph graphs/{repo}/graphify-out/graph.json
graphify path "A" "B" --graph graphs/{repo}/graphify-out/graph.json
graphify explain "N" --graph graphs/{repo}/graphify-out/graph.json
```
