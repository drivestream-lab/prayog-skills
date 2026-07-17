# engg-reviews — Implementation Plan (MVP → Standardize)

**Status:** Phase 1 in progress on `features/rc-2`  
**Branch:** `features/rc-2` (local only — no PR)  
**Parent version:** 0.4.3 → experimental `0.5.0-rc.2` on `features/rc-2` only  

---

## 1. Goal

Give PE a **gate-independent** way to map an open **meta PRD PR** onto a **fleet of app repos** using **in-depth code-graph evidence**, then ask **product/feature questions on the meta PR** so PM can strengthen the PRD.

**Out of scope for this work:** changing Gate 1/2, `impact-map-*` / `spec-*` labels, or `sdd-delivery/v2` navigation in [`workflow.yaml`](../workflow.yaml).

**Success (Phase 1):** One PE on one real meta Draft PR produces better product questions (scenario / example / recommendation / why) grounded in as-built + Graphify evidence — PM can answer without reading code.

---

## 2. Principles (locked)

| Principle | Meaning |
|-----------|---------|
| Two phases | Local MVP first; Docker/FalkorDB/MCP only if value is proven |
| Adjunct system | `engg-reviews` — does **not** unlock Gate 1 or `/spec-draft` |
| OSS evidence | Graphify = codegraph provider (Phase 1: local CLI/skill) |
| In-depth | Per-capability `query` / `path` / `explain`; prefer `EXTRACTED` edges |
| Artifacts > chat | Durable meta report; PR comments are projections |
| Provider-abstract | Skills target a “codegraph provider” interface so Phase 2 does not rewrite skills |
| Experimental in-tree | Under `skills/engg-reviews/`; **not** listed in `profiles/*.yaml` skill lists |

---

## 3. Phase split

```text
Phase 1 — Local MVP (evaluate value)
  features/rc-2 branch, no PR
  engg-reviews skills + local Graphify
  PE cwd = {fleet}/pe-workspace/ (graphs under graphs/{repo}/)
  Meta + apps = sibling clones; graphs not left in app trees
  Measure: question quality + PE/PM feedback

Phase 2 — Standardize (only if Phase 1 wins)
  Distribute engg-reviews skills to PE team
  Shared codegraph service: Docker + FalkorDB + Graphify MCP
  Same skill contract; switch provider to MCP
  Optional: Launchpad advisory_skills later
```

---

## 4. Architecture (Phase 1)

```text
Meta Draft PR (gate may be pending — OK)
    │
    ├─ SDD path (unchanged)
    │    validate → impact-map → Gate1 → merge → spec-draft → …
    │
    └─ engg-reviews (parallel, anytime PR open)
         /ensure-repo-graph
              PE: sibling clones @ develop
              local Graphify build/refresh → graphify-out/
         /prd-codebase-map
              PRD × as-built × graph evidence
              → prd/reports/PRD-Codebase-Map-{INIT}.md
         /post-product-questions
              PE posts Qs + recommendations on Meta PR; asks PM feedback
         NEVER sets impact-map-* / spec-* labels
         PM (later): PR thread → update PRD/outline → requirements skills
```

### Codegraph provider interface (write once)

Skills call this abstract contract:

| Operation | Phase 1 (local) | Phase 2 (shared) |
|-----------|-----------------|------------------|
| `ensure_graph(repo, sha)` | `graphify <path> [--mode deep] [--update]` | Sync worker + FalkorDB refresh |
| `query(repo, question)` | `graphify query "…"` | MCP `query_graph` |
| `path(repo, a, b)` | `graphify path A B` | MCP `shortest_path` |
| `explain(repo, node)` | `graphify explain N` | MCP `explain` / `get_node` |
| `freshness` | `develop_sha` + `graph_digest` of `graph.json` | Same fields from service |

**No Docker in Phase 1.** Neo4j/FalkorDB optional push is deferred to Phase 2.

---

## 5. Skills to author (Phase 1)

### 5.1 Layout on `features/rc-2`

```text
skills/engg-reviews/
  README.md                          # experimental; not part of sdd-delivery/v2
  references/
    codegraph-provider.md            # abstract ops + local Graphify mapping
    handoff-adjunct.md               # egg→engg adjunct handoff schema
    product-question-template.md     # scenario / example / recommend / why / alternatives
  ensure-repo-graph/
    SKILL.md
    references/
      output-template.md             # fleet graph status table
  prd-codebase-map/
    SKILL.md
    references/
      checks.md
      layout-defaults.md             # meta reports_dir; sibling clone convention
      output-template.md             # PRD-Codebase-Map artifact
      governance.md                  # product-only questions; eng appendix
  post-product-questions/
    SKILL.md
    references/
      output-template.md             # Meta PR comment body
```

Bump on branch only: `VERSION` → `0.5.0-rc.2`.  
Do **not** add skills to [`profiles/meta-pm.yaml`](../profiles/meta-pm.yaml) or app `development_skills`.  
Do **not** add Gate edges in [`workflow.yaml`](../workflow.yaml).

### 5.2 `/ensure-repo-graph`

**Purpose:** Make local Graphify graphs fresh for the candidate fleet.

**Steps:**
1. Resolve candidate repos (Impact-Map affected list if present; else PE-supplied list / catalog hint).
2. Ensure each repo is a sibling clone at `develop` (fetch + checkout; record SHA).
3. Per repo: if `graphify-out/graph.json` missing → `graphify <path> --mode deep --no-viz` (or `/graphify`); if stale vs `develop` SHA → `graphify <path> --update`.
4. Emit fleet status table + adjunct handoff (`outcome: pass|blocked`).

**Non-goals:** no product questions; no GitHub writes; no gate labels.  
**If Graphify missing:** `blocked` with install steps (`uv tool install graphifyy`) — no fake deep PASS.

### 5.3 `/prd-codebase-map` (core)

**Purpose:** Map meta PRD capabilities onto fleet graphs + as-built; emit PM-facing questions.

**Inputs:**
- Meta: `prd/INIT-*.md`, meta PR head SHA, PRD digest  
- Optional: `prd/reports/Impact-Map-*.md` (candidates only)  
- Per repo `@ develop`: as-built, Accepted ADRs (product-relevant), `graphify-out/`  

**Per capability protocol:**
1. Derive product-language query terms from PRD capability.  
2. Provider `query` → communities/nodes; `path` / `explain` for critical links.  
3. Prefer **EXTRACTED**; **INFERRED** / **AMBIGUOUS** → question, not fact.  
4. Diff vs as-built → `exists | partial | absent | conflict | unknown`.  
5. Product questions only for `partial` / `conflict` / high-impact `unknown` (cap + prioritize).  

**Output:** `prd/reports/PRD-Codebase-Map-{INIT}.md` (revisioned)

Required sections:
- Fleet graph status (`repo`, `develop_sha`, `graph_digest`, freshness)  
- Capability matrix (PRD ref | as-built | graph evidence | confidence | delta)  
- Product questions (see template below)  
- Eng appendix (paths/communities — not for PM decision UI)  
- Adjunct handoff: `contract: engg-reviews/v1`, `next_candidates: [post-product-questions]` or `[]` — **never** `gate-1` / `prd-merge` / `spec-draft`  

**Greenfield / empty as-built:** short-circuit to PRD-ambiguity questions only; do not claim codebase grounding.

### 5.4 `/post-product-questions` (PE)

**Purpose:** Publish map product questions on the **Meta PR** with PE
recommendations and an explicit ask for **PM feedback**. Does **not** collect
PM decisions interactively and does **not** edit the PRD.

**Input:** `PRD-Codebase-Map-*.md` + Meta PR number.  
**Output:** `Meta-PR-Product-Questions-{INIT}.md` + `gh pr comment` (authorized).

PM later: read PR → update PRD/outline → requirements skills.

### 5.5 Product question template (minimum fields)

```markdown
### Q-{NN} — {short title}
- **PRD ref:** …
- **Delta:** partial | conflict | unknown
- **Scenario:** When {actor} does {action}…
- **Example:** …
- **Recommendation:** …
- **Why:** …
- **Alternatives:** …
- **Evidence:** repo / node-or-path / EXTRACTED|INFERRED / as-built row
```

---

## 6. Adjunct handoff (non-delivery)

```yaml
handoff:
  contract: engg-reviews/v1
  stage: prd-codebase-map   # or ensure-repo-graph | post-product-questions
  outcome: pass | findings | needs-input | blocked | stale | failed | skipped
  artifact:
    path: prd/reports/PRD-Codebase-Map-{INIT}.md
    digest: sha256:{hex}
  blockers: []
  signals:
    gate_coupled: false
    codegraph_provider: local-graphify   # phase2: mcp-falkordb
  next_candidates: []                    # or [post-product-questions]
  human_checkpoint: true
  external_action: false
```

Navigators of `sdd-delivery/v2` **ignore** `engg-reviews/v1` for Gate transitions.

---

## 7. Phase 1 implementation sequence

| Step | Work | Done when |
|------|------|-----------|
| 0 | Create branch `features/rc-2` from current default; set `VERSION` to `0.5.0-rc.2` | Branch exists locally |
| 1 | Add `skills/engg-reviews/README.md` + `references/codegraph-provider.md` + `handoff-adjunct.md` + `product-question-template.md` | Contracts reviewable |
| 2 | Author `/ensure-repo-graph` SKILL + output template | PE can refresh fleet graphs via skill text |
| 3 | Author `/prd-codebase-map` SKILL + checks + output template + governance | Full map protocol written |
| 4 | Author `/post-product-questions` (PE → Meta PR; not PM interactive) | PE post skill written |
| 5 | Spike on one real meta PR + 2–3 app repos | Manual/skill run; map + ≤10 product questions |
| 6 | PE + PM feedback | Keep / iterate / kill decision |
| 7 | Tighten templates from spike learnings | MVP “good enough” on `features/rc-2` |

**Explicit non-steps in Phase 1:** no Docker, no FalkorDB, no MCP server, no PR, no profile/workflow Gate edits, no Launchpad pin bump.

---

## 8. Phase 1 evaluation rubric

| Signal | Positive | Negative |
|--------|----------|----------|
| PE time | Less thrash than ad-hoc repo reading | Graph refresh dominates; no better questions |
| Question quality | PM answers in feature language without code | Questions are eng jargon or graph noise |
| PRD impact | Concrete PRD edits from resolutions | Report unused; Gate 1 unchanged in practice |
| Confidence | EXTRACTED-backed rows trusted | Too many INFERRED-only “facts” |

**Go to Phase 2 only if** ≥2 of {PE time, question quality, PRD impact} are clearly positive.

---

## 9. Phase 2 (outline only — after go decision)

1. Package/distribute `engg-reviews` skills to PE team (skills CLI or Launchpad `advisory_skills`).  
2. Docker Compose: repo sync workers (catalog / impact-map fleet) + Graphify refresh + FalkorDB + Graphify MCP.  
3. PE setup: MCP endpoint + skills only (no daily fleet clone).  
4. Point `codegraph-provider` at `mcp-falkordb`; keep local Graphify as offline fallback.  
5. AuthZ + freshness SLA + pinned Graphify version (security review).  
6. Still never mutate Gate labels from the service.

---

## 10. Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Graphify skill supply-chain / security ratings | Pin version; prefer CLI over unreviewed skill copy; document install |
| Graph noise → question spam | Cap questions; prioritize conflict/partial; INFERRED ≠ fact |
| Accidental Gate coupling | `gate_coupled: false`; no profile registration; README non-negotiables |
| Multi-repo toil in Phase 1 | Limit spike to 2–3 repos; accept PE sync as MVP cost |
| Consistency script noise | Keep engg-reviews tokens out of SDD invariants until promote |

---

## 11. Review checklist (for you)

- [ ] Phase 1 local-only / Phase 2 standardize-only-if-value — agree?  
- [ ] Three skills (ensure-graph, map, review-questions) — review-questions deferrable for spike?  
- [ ] Artifact on meta `prd/reports/PRD-Codebase-Map-*` — agree?  
- [ ] Codegraph provider abstraction — agree?  
- [ ] No `workflow.yaml` / profile / Gate changes on `features/rc-2` — agree?  
- [ ] Evaluation rubric sufficient to decide Phase 2?  

---

## 12. Proposed first commit scope (after plan approval)

On `features/rc-2` only:

1. `VERSION` → `0.5.0-rc.2`  
2. Scaffold `skills/engg-reviews/**` as in §5.1 (SKILL.md + references; no Docker)  
3. `docs/engg-reviews-implementation-plan.md` (this file)  

No PR. No profile updates.
