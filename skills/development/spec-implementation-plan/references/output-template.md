---
goal: {INITIATIVE} — implementation plan
initiative: {INITIATIVE}
status: Planned
date_created: {YYYY-MM-DD}
source_spec: {SPEC_PATH}
source_spec_digest: sha256:{hex}
feasibility_report: {FEASIBILITY_PATH or N/A}
feasibility_digest: sha256:{hex or N/A}
technical_review: {TECHNICAL_REVIEW_PATH or N/A}
technical_review_digest: sha256:{hex or N/A}
prd_digest: sha256:{hex}
impact_map: {IMPACT_MAP_PATH}
impact_map_revision: {N}
repo_scope_digest: sha256:{hex}
approved_meta_pr_head: {SHA}
branch: chore/INIT-{COMPONENT}-{NUMBER}-spec-{repo}
review_deadline: {YYYY-MM-DD + 3 business days}
deciders: PE — spec-lgtm + Approve on exact head after full package
---

# Implementation plan — {INITIATIVE}

## Source freshness and command contract

| Item | Value | Status |
|------|-------|--------|
| Spec / digest | `{SPEC_PATH}` / `sha256:{hex}` | CURRENT / STALE |
| Feasibility / digest | `{FEASIBILITY_PATH}` / `sha256:{hex}` | CURRENT / STALE |
| Technical review / digest | `{TECHNICAL_REVIEW_PATH or N/A}` / `sha256:{hex or N/A}` | CURRENT / STALE / N/A |
| Impact map / revision | `{IMPACT_MAP_PATH}` / `{N}` | CURRENT / STALE |
| Repo scope digest | `sha256:{hex}` | CURRENT / STALE |
| Approved meta PR head | `{SHA}` | CURRENT / STALE |
| `check_command` | `{command}` | RESOLVED / MISSING |
| `test_command` | `{command}` | RESOLVED / MISSING |
| `verify_command` | `{command or N/A — reason}` | RESOLVED / N/A / MISSING |
| `ground_command` | `{command or N/A — reason}` | RESOLVED / N/A / MISSING |
| UI lock / digest | `{LOCKED path or N/A — non-UI}` / `sha256:{hex or N/A}` | CURRENT / STALE / N/A |
| Explore cleanup | all temporary variants removed | PASS / FAIL / N/A |

> Do not continue if any source is STALE or required command is MISSING.
> Do not continue if UI is in scope and lock is missing, STALE, or explore cleanup FAIL.

## 0. Technical design reference

| Item | Value |
|------|-------|
| Technical review | {path to Technical-Review-{initiative}.md or "N/A — no NEW-ADR findings"} |
| PE sign-off | {[ ] required / [x] complete — date} |
| Resolved ADRs | {adr_dir/adr-NNN-slug.md (link, Status: Accepted), … or N/A — canonical files created by `/spec-technical-review` and accepted before planning; TDD §4 index refs alone are not sufficient} |
| UI lock | {path to LOCKED-{INIT}.md — Selected + Improvements, or "N/A — non-UI / ui-variations skipped"} |
| Outstanding PM questions | {list or "none — all resolved"} |
| Outstanding domain questions | {list or "none — all resolved"} |

> Do not start W0 implementation until PE sign-off is marked complete above.

---

## 1. Requirements (REQ)

| ID | Source (spec) | Summary | Feasibility ref |
|----|---------------|---------|-----------------|
| REQ-W0 | | | |

---

## 2. Implementation phases

### Phase W0 — {title}

**GOAL-W0:** …

| Task | Description | Codebase | Spec path | Done when | Verify command | MDC notes | ADR notes | Branch |
|------|-------------|----------|-----------|-----------|----------------|-----------|-----------|--------|
| TASK-W0-01 | | {repo} | {SPEC_PATH} | | `{check_command}` | | | |

#### Files (W0)

| ID | Path | Action |
|----|------|--------|
| FILE-W0-01 | | create / edit |

#### Tests (W0)

| ID | Layer | Command | Proves |
|----|-------|---------|--------|
| TEST-W0-U | unit | (from tests_readme / profile) | |

---

### Phase W1 — {title}

**GOAL-W1:** …

| Task | Description | Codebase | Spec path | Done when | Verify command | MDC notes | ADR notes | Branch |
|------|-------------|----------|-----------|-----------|----------------|-----------|-----------|--------|
| TASK-W1-01 | | {repo} | {SPEC_PATH} | | | | | |

#### Files (W1)

| ID | Path | Action |
|----|------|--------|

#### Tests (W1)

| ID | Layer | Command | Proves |
|----|-------|---------|--------|

(Repeat per wave.)

---

## 3. Dependencies (DEP)

| ID | Dependency | Blocks |
|----|------------|--------|

---

## 4. Risks (RISK)

| ID | Risk | Mitigation |
|----|------|------------|

---

## 5. Out of scope

- …

---

## 6. As-built and docs tasks

> Update these in the **same PR** as the code they describe.

| Task | File | Action |
|------|------|--------|
| Update implementation-status.md | `docs/specification/as-built/implementation-status.md` | mark wave in_progress → complete |
| Update tests/README.md | `tests/README.md` | add verify commands for new scripts |

> **ADR lifecycle** — Draft and Accepted ADR files are created and accepted during
> `/spec-technical-review` and the `technical-review-approval` checkpoint.
> Planning consumes Accepted files only; do not add ADR promotion tasks here.

---

## 7. Plan check summary

| Check | Status |
|-------|--------|
| P1–P14 | |

---

## 8. PR instructions

> Commit this plan to the **Draft spec PR** branch alongside spec, feasibility,
> and TDD. Label remains **`spec-pending`** until PE completes §10.

```
Branch:   chore/INIT-{COMPONENT}-{NUMBER}-spec-{repo}  (Draft PR)
PR title: "[INIT-{COMPONENT}-{NUMBER}] Spec — {repo}"
PR body:  link meta PRD PR; paste §1 Requirements table + wave goals summary

Required reviewers: @{pe-team}
Review deadline: {date from front matter}

PE checklist (before spec-lgtm):
  [ ] Spec + feasibility + TDD + Accepted ADRs + this plan on current head
  [ ] §0 PE sign-off on TDD marked complete (or N/A with reason)
  [ ] Wave order and dependencies make sense
  [ ] Done-when criteria are observable and testable
  [ ] WorkManifest YAML (§9) correct — wave IDs W0, W1, … (one issue per wave)
  [ ] P1–P14 checks all pass

After spec-lgtm + Approve + merge — **`/board-seed`** from §9 (post-merge only):
  Create one GitHub Issue per wave (W0, W1, …) using §9 titles, bodies, depends_on
  Search for existing initiative/wave issues first; create only missing issues
  Then: /pre-implement → /loop-spec → /verify (when applicable) → /ground-spec
```

---

## 10. Gate 2 unlock (PE — after plan on head)

Present this section in chat when the plan is committed. **No GitHub side
effects** until PE completes the unlock.

| Item | Value |
|------|-------|
| Verdict | GATE OPEN REQUEST / BLOCKED |
| Spec PR | {URL} |
| Spec PR head SHA | `{SHA}` |
| Gate label (current) | `spec-pending` |
| Gate label (target) | `spec-lgtm` |
| Blocking items | none / {reason} |

Provision labels when missing:

```bash
launchpad apply-gates --repo <name> --apply
```

PE actions (all on **exact current head**):

1. Remove `spec-pending`, `spec-blocked`, `spec-revised`, `spec-stale`; add **`spec-lgtm`**
2. Submit GitHub **Approve** with attestation body (below)
3. Mark Draft PR **Ready for review**
4. Authorize merge (human or policy); then **`/board-seed`** from §9

### Approve attestation body

```text
Spec package approved
initiative: {INIT-id}
spec_pr_head_sha: {SHA}
meta_pr_head_sha: {SHA}
impact_map_revision: {N}
prd_digest: sha256:{hex}
scope_digest: sha256:{hex}
plan_digest: sha256:{hex}
artifacts:
  - docs/specification/product/INIT-{id}.md
  - docs/specification/reports/Initiative-Feasibility-Report-{INIT-id}.md
  - docs/specification/reports/Technical-Review-{INIT-id}.md
  - docs/specification/reports/Implementation-Plan-{INIT-id}.md
```

Never infer approval from `spec-lgtm` alone — Approve, label, and artifact
digests must match the same head SHA.

| PE action | Remove | Add |
|-----------|--------|-----|
| Pending/new revision | `spec-lgtm`, `spec-blocked` | `spec-pending` |
| Request changes/hold | `spec-pending`, `spec-lgtm` | `spec-blocked` |
| Approve full package | `spec-pending`, `spec-blocked`, `spec-revised`, `spec-stale` | `spec-lgtm` |

---

## 9. WorkManifest seed

> **Primary:** dev creates **one GitHub Issue per wave** (`W0`, `W1`, …) from this section.
> Use §9 `title`, `body`, and `depends_on` when running `gh issue create`.
>
> Before creation, run `gh auth status` and search existing issues by initiative
> plus wave id. With explicit developer authorization, create only missing
> issues. If `gh` is unavailable, output exact commands and stop.
>
> Wave `id` must be exactly `W0`, `W1`, … — one issue per wave, not per TASK row.
> Set `target.org` from governance and `target.project` from
> `governance.project_board.name` (read-only meta). Resolve with
> `launchpad board-bind --client <id>` — do not free-text board names.

```yaml
# Generated by /spec-implementation-plan — {DATE}
# LOCAL — do not commit to prayog-skills upstream
apiVersion: launchpad/v1
kind: WorkManifest

initiative: {INITIATIVE}
# Branch naming: feature/INIT-{COMPONENT}-{NUMBER}-w{N}-{slug}
#   COMPONENT = service branch_code from service-catalog.yaml (2-7 uppercase chars)
#   NUMBER    = initiative sequence number (1-7 digits, e.g. 001, 0012)
#   N         = wave number (0, 1, 2, …) — expected by convention; advisory in CI regex
#   slug      = lowercase kebab description (e.g. ingestion-pipeline, jwt-login)

metadata:
  title: {INITIATIVE} — {spec title}
  summary: |
    {2–3 sentence summary from spec}
  playbook:
    - {SPEC_PATH}
    - docs/specification/reports/Implementation-Plan-{INITIATIVE}.md

target:
  org: {github-org}
  project: {GitHub Project name}

defaults:
  initiative: {INITIATIVE}
  parent: EPIC
  status: Backlog
  labels:
    - {initiative-label}

epic:
  id: EPIC
  repo: {meta-repo or primary codebase repo}
  title: "[feature] {INITIATIVE} — {short title}"
  codebase: {repo}
  spec_path: {SPEC_PATH}
  verify_command: {make verify or profile verify command}
  body: |
    ## Objective

    {GOAL from spec — 2–3 sentences}

    ## Waves

    | Wave | Goal |
    |------|------|
    | W0 | {GOAL-W0} |
    | W1 | {GOAL-W1} |

    ## References

    - Spec: {SPEC_PATH}
    - Implementation plan: docs/specification/reports/Implementation-Plan-{INITIATIVE}.md
    - Technical review: docs/specification/reports/Technical-Review-{INITIATIVE}.md (if applicable)

work:
  # ── Wave W0 (one issue per wave — id must be W0, not W0-DESIGN) ─────────
  - id: W0
    kind: issue
    repo: {codebase repo}
    title: "[{INITIATIVE} W0] {wave W0 goal or summary title}"
    depends_on: []
    codebase: {repo}
    spec_path: {SPEC_PATH}
    verify_command: {wave W0 verify command or make verify}
    status: Backlog
    body: |
      ## Wave goal

      {GOAL-W0 from spec}

      ## Tasks (from plan §2)

      - {TASK-W0-01}: {done-when summary}
      - {TASK-W0-02}: {done-when summary}

      ## Done when

      - [ ] All W0 tasks complete per plan

      ## Spec reference

      {SPEC_PATH}

  # ── Wave W1 ──────────────────────────────────────────────────────────────
  - id: W1
    kind: issue
    repo: {codebase repo}
    title: "[{INITIATIVE} W1] {wave W1 goal or summary title}"
    depends_on:
      - W0
    codebase: {repo}
    spec_path: {SPEC_PATH}
    verify_command: {wave W1 verify command}
    status: Backlog
    body: |
      ## Wave goal

      {GOAL-W1 from spec}

      ## Tasks (from plan §2)

      - {TASK-W1-01}: {done-when summary}

      ## Done when

      - [ ] All W1 tasks complete per plan

      ## Spec reference

      {SPEC_PATH}

  # (one work: entry per wave — NOT one per TASK row)
```
