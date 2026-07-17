---
name: ensure-repo-graph
description: >-
  Phase 1 engg-reviews: ensure local Graphify code graphs are present and fresh
  for a fleet of candidate app repos at develop. Resolves candidates from an
  Impact-Map or PE list, syncs sibling clones, builds or updates graphify-out/,
  and records develop_sha + graph_digest. Gate-independent — never sets
  impact-map-* or spec-* labels. Run before /prd-codebase-map.
disable-model-invocation: true
paths: prd/reports/**, config/service-catalog.yaml
metadata:
  background_eligible: false
  experimental: true
  pack: engg-reviews
---

# Ensure repo graph

Make **in-depth code graphs** available for the candidate fleet so
`/prd-codebase-map` can ground the PRD. **Do not** ask product questions.
**Do not** touch SDD gates.

Provider contract: [../references/codegraph-provider.md](../references/codegraph-provider.md).  
Handoff: [../references/handoff-adjunct.md](../references/handoff-adjunct.md).

## NON-NEGOTIABLE

1. This skill is **gate-independent**. Never create/update/delete `impact-map-*`
   or `spec-*` labels. Never claim Gate 1 readiness.
2. Use the **codegraph provider** interface. Phase 1 default: local Graphify CLI.
3. If Graphify (or configured provider) is missing → outcome `blocked` with
   install steps. **No PASS** and no “light skim” substitute.
4. Each repo must be on integration branch (default `develop`) at a recorded SHA
   before build/update.
5. Prefer `--mode deep` for first build; `--update` when graph exists but SHA
   changed.
6. Record per-repo `develop_sha` + `graph_digest` (sha256 of `graph.json`).
7. No product questions. No PRD edits. No app PRs. No GitHub writes unless the
   user later authorizes unrelated actions outside this skill.
8. Dual output: chat fleet table + optional saved status snippet under meta
   `prd/reports/` when useful (`Graph-Fleet-Status-{INIT}.md`).

## Inputs

1. **Initiative id** — (REQUIRED) e.g. `INIT-001`
2. **Candidate repos** — (REQUIRED) from one of:
   - `prd/reports/Impact-Map-{INIT}.md` affected (+ optional transitive) list
   - PE-supplied list
   - `config/service-catalog.yaml` hint (only if PE confirms)
3. Workspace layout — **preferred:** `{fleet}/pe-workspace/` with
   `fleet.yaml` + `graphs/{repo}/`; app code at `../{repo}`; meta at
   `../drivestream-meta` (or `{client}-meta`). Legacy: cwd = meta with
   sibling `../{repo}` graphs (discouraged — pollutes app trees).
4. **Integration branch** — default `develop`

## Process

### T0 — Gather

- Prefer cwd = **pe-workspace** (or PE states `fleet.yaml` path).
- Resolve candidate repo list from impact-map / `fleet.yaml` initiatives /
  PE list.
- Cap spike fleets at a reasonable size (document if >5 repos).

### T1 — Provider check

```bash
command -v graphify || uv tool run --from graphifyy graphify --help
```

If unavailable:

```text
blocked: install with `uv tool install graphifyy` (PyPI package graphifyy),
then re-run /ensure-repo-graph.
```

Stop with handoff outcome `blocked`.

### T2 — Sync clones

For each candidate repo:

1. Resolve `code_path` from `fleet.yaml` or `../{repo}` relative to fleet root.
2. If missing: clone (only with explicit PE authorization).
3. `git fetch` + checkout integration branch; record `develop_sha`.
4. Fail that row as `blocked` if dirty tree would mislead SHA policy — ask PE
   to stash/clean or confirm.

### T3 — Ensure graph

Prefer pe-workspace helper when present:

```bash
./bin/refresh-graph.sh {repo}            # deep → graphs/{repo}/graphify-out/
./bin/refresh-graph.sh {repo} --update   # when graph exists
```

Otherwise, for each repo:

1. Build Graphify in `code_path`, then **copy** `graphify-out/` to
   `graphs/{repo}/graphify-out/` and remove it from the app clone.
2. Compute `graph_digest`; write `graphs/{repo}/.engg-reviews-meta.json`.
3. Status: `CURRENT` | `BUILT` | `UPDATED` | `FAILED`

Canonical query path: `graphs/{repo}/graphify-out/graph.json`  
(not `{code_path}/graphify-out/`).

### T4 — Report

Present [references/output-template.md](references/output-template.md).  
Append adjunct handoff (`stage: ensure-repo-graph`).

| Outcome | When | next_candidates |
|---------|------|-----------------|
| `pass` | All required candidates CURRENT/BUILT/UPDATED | `prd-codebase-map` |
| `blocked` | Provider missing or any required repo failed | `[]` or retry ensure |
| `needs-input` | Candidate list unclear | `[]` |
| `failed` | Unexpected tool error | `[]` |

## Forbidden next_candidates

Never: `gate-1`, `prd-merge`, `spec-draft`, or any `sdd-delivery/v2` node.

## Workflow handoff

Append the envelope from
[../references/handoff-adjunct.md](../references/handoff-adjunct.md).
Use `contract: engg-reviews/v1` and stage `ensure-repo-graph`.

| Outcome | Next |
|---------|------|
| `pass` | `/prd-codebase-map` |
| `blocked` / `failed` / `needs-input` | Fix provider/clones; re-run `/ensure-repo-graph` |

Always `gate_coupled: false`. This handoff must **not** be used to navigate
`sdd-delivery/v2` Gate 1/2.
