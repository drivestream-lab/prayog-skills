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
deciders: Dev team lead — explicit LGTM required
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

> Do not continue if any source is STALE or required command is MISSING.

## 0. Technical design reference

| Item | Value |
|------|-------|
| Technical review | {path to Technical-Review-{initiative}.md or "N/A — no NEW-ADR findings"} |
| PE sign-off | {[ ] required / [x] complete — date} |
| Resolved ADRs | {adr_dir/adr-NNN-slug.md (link), … or N/A — must be adr_dir file paths, not TDD section refs} |
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
| TASK-SPEC-ADR-NN (one row per NEW-ADR) | `docs/specification/adr/adr-NNN-{slug}.md` | promote TDD §4.N draft → Accepted ADR file; set status Accepted + PE name + date; update TDD §4.N status from Draft → Accepted (conditional: include only when NEW-ADR findings exist; pre-W0) |

> **Accepted ADR file format** — use this structure when writing each `adr_dir` file:
>
> ```markdown
> # ADR-{NNN} — {short title}
>
> | Field  | Value |
> |--------|-------|
> | Status | Accepted |
> | Date   | {YYYY-MM-DD of PE Approve} |
> | PE     | @{pe-name} |
> | TDD    | {path to Technical-Review-{initiative}.md} §4.{n} |
>
> ## Context
> {Problem statement from TDD §4.N}
>
> ## Decision
> {Chosen option + one-sentence rationale from TDD §4.N Recommendation}
>
> ## Consequences
> {From TDD §4.N Consequences}
> ```
>
> The acceptance date and PE name come from the GitHub Approve event on the spec PR —
> not from the date the file is written.

---

## 7. Plan check summary

| Check | Status |
|-------|--------|
| P1–P14 | |

---

## 8. PR instructions

> Commit this plan to the spec PR branch alongside spec, feasibility, and TDD.
> Dev lead GitHub Approve on spec PR = gate satisfied. **Merge spec PR**, then seed board.

```
Branch:   chore/INIT-{COMPONENT}-{NUMBER}-spec-{repo}
PR title: "[INIT-{COMPONENT}-{NUMBER}] Spec — {repo}"
PR body:  link meta PRD PR; paste §1 Requirements table + wave goals summary

Required reviewers (CODEOWNERS): @{dev-team-lead} · @{pe-team} (when TDD present)
Review deadline: {date from front matter}

Reviewer checklist:
  [ ] §0 PE sign-off on TDD is marked complete (or N/A with reason)
  [ ] Wave order and dependencies make sense
  [ ] Done-when criteria are observable and testable
  [ ] WorkManifest YAML (§9) looks correct — wave IDs are W0, W1, … (one issue per wave)
  [ ] P1–P14 checks all pass

After spec PR merge — dev seeds board from §9 (post-merge only):
  Create one GitHub Issue per wave (W0, W1, …) using §9 titles, bodies, depends_on
  Search for existing initiative/wave issues first; create only missing issues
  Then start wave coding: /pre-implement → /loop-spec → /verify (when applicable) → /ground-spec
```

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
> Update `target.org` and `target.project` to match the GitHub org and Project name.

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
