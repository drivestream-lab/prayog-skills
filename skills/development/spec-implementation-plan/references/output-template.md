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
| `verify_command` | `{live script under live_verify_dir, or N/A — reason}` | RESOLVED / N/A / MISSING |
| `ground_command` | `{command or N/A — reason}` | RESOLVED / N/A / MISSING |

> Do not continue if any source is STALE or required command is MISSING.
> `verify_command` is **live** verify (human-run at checkpoint `live-verify`),
> not `{test_command}`. When P15 applies, N/A is invalid — co-ship a FILE under
> `live_verify_dir` in the same wave.

## 0. Technical design reference

| Item | Value |
|------|-------|
| Technical review | {path to Technical-Review-{initiative}.md or "N/A — no NEW-ADR findings"} |
| PE sign-off | {[ ] required / [x] complete — date} |
| Resolved ADRs | {adr_dir/adr-NNN-slug.md (link, Status: Accepted), … or N/A — canonical files created by `/spec-technical-review` and accepted before planning; TDD §4 index refs alone are not sufficient} |
| Outstanding PM questions | {list or "none — all resolved"} |
| Outstanding domain questions | {list or "none — all resolved"} |

> Do not start W0 implementation until PE sign-off is marked complete above.

---

## 1. Requirements (REQ) — product ids

Cite **product** `REQ-*` from the spec (same ids as PRD/spec). Do **not** invent
wave-scoped shadow ids like `REQ-W{n}`.

| ID | Summary | Spec path | Waves |
|----|---------|-----------|-------|
| REQ-01 | | {SPEC_PATH} | W0 |
| REQ-02 | | {SPEC_PATH} | W0, W1 |

---

## 2. Implementation phases

### Phase W0 — {title}

**GOAL-W0:** …

| Task | Description | Implements | Depends on | Files (path/action) | Exit criteria | Proof (kind / command\|review) | Expected | Evidence expected | Codebase | Spec path | Verify command | MDC notes | ADR notes | Branch |
|------|-------------|------------|------------|---------------------|---------------|--------------------------------|----------|-------------------|----------|-----------|----------------|-----------|-----------|--------|
| TASK-W0-01 | | REQ-01, REQ-02 | — | `src/…` create | observable result | command / `{check_command}` | exit 0 + assertion | Wave-Execution-… § TASK-W0-01 | {repo} | {SPEC_PATH} | `{check_command}` | | | |

#### Files (W0)

| ID | Path | Action |
|----|------|--------|
| FILE-W0-01 | | create / modify / delete / inspect |

#### Tests (W0)

| ID | Layer | Command | Proves |
|----|-------|---------|--------|
| TEST-W0-U | unit | (from tests_readme / profile) | REQ-* / TASK-* |
| TEST-W0-I | integration/contract | (when applicable) | REQ-* / TASK-* |
| TEST-W0-L | live (smoke\|sandbox) | `{live_verify_dir}/…` (human-run) | new/changed product surface (P15) |

#### Verification Coverage (W0)

Map every in-scope acceptance criterion / REQ for this wave to exactly one
primary layer (and note secondary layers if needed):

| REQ / criterion | unit | integration/contract | smoke | sandbox | Notes |
|-----------------|------|----------------------|-------|---------|-------|
| REQ-01 / … | TEST-W0-U | N/A | TEST-W0-L | N/A | |

#### Live-verification intent (W0)

Planning records **intent** only. Bind actual runtime head / build SHA and
record observed evidence at human checkpoint `live-verify` — do not invent them
here.

| Field | Value |
|-------|-------|
| Applicable | yes / no — {reason if no} |
| Environment class | local-compose / staging-sandbox / … |
| Mode | smoke \| sandbox |
| Runtime head binding | Bound at `live-verify` against the wave PR head under test (not filled at planning) |
| Prerequisites | |
| Safe test data | |
| Steps / command | `{live_verify_dir}/…` |
| Expected observations | |
| Expected evidence | `Live-Verify-{INIT}-W0.md` |
| Cleanup | |
| Stop conditions | |

> When the wave FILE list adds/changes a product surface (P15), include ≥1
> `live_verify_dir` FILE in **Files** and a live row here. Agent implements the
> script; human executes it at `live-verify`.

---

### Phase W1 — {title}

**GOAL-W1:** …

| Task | Description | Implements | Depends on | Files (path/action) | Exit criteria | Proof (kind / command\|review) | Expected | Evidence expected | Codebase | Spec path | Verify command | MDC notes | ADR notes | Branch |
|------|-------------|------------|------------|---------------------|---------------|--------------------------------|----------|-------------------|----------|-----------|----------------|-----------|-----------|--------|
| TASK-W1-01 | | REQ-{nn} | — | | | | | | {repo} | {SPEC_PATH} | | | | |

#### Files (W1)

| ID | Path | Action |
|----|------|--------|

#### Tests (W1)

| ID | Layer | Command | Proves |
|----|-------|---------|--------|

#### Verification Coverage (W1)

| REQ / criterion | unit | integration/contract | smoke | sandbox | Notes |
|-----------------|------|----------------------|-------|---------|-------|

#### Live-verification intent (W1)

| Field | Value |
|-------|-------|
| Applicable | |
| Environment class | |
| Mode | |
| Runtime head binding | Bound at `live-verify` (not planning) |
| Prerequisites | |
| Safe test data | |
| Steps / command | |
| Expected observations | |
| Expected evidence | |
| Cleanup | |
| Stop conditions | |

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
| Update tests/README.md | `tests/README.md` | add live-verify commands for co-shipped scripts |

> **ADR lifecycle** — Draft and Accepted ADR files are created and accepted during
> `/spec-technical-review` and the `technical-review-approval` checkpoint.
> Planning consumes Accepted files only; do not add ADR promotion tasks here.

---

## 7. Plan check summary

| Check | Status |
|-------|--------|
| P1–P16 | |

---

## 8. Forge / PR instructions

> Persist this plan locally and publish via `/commit-workspace` (or Gateflow
> ForgeClient) to the **Draft spec PR** branch alongside spec, feasibility,
> and TDD. Do **not** commit inside this skill. Label remains **`spec-pending`**
> until PE completes §10.

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
  [ ] Done-when / exit criteria are observable and testable (P4)
  [ ] Verification Coverage maps every criterion to a layer (P5)
  [ ] WorkManifest YAML (§9) passes workmanifest-contract-pass (P16) — prayog/v1
  [ ] P1–P16 checks all pass (including P15 co-ship when surface changes)

After spec-lgtm + Approve + merge — **`/create-board-tickets`** from §9 (post-merge only):
  Create one GitHub Issue per wave (W0, W1, …) using §9 titles, bodies, depends_on
  Search for existing initiative/wave issues first; create only missing issues
  Then Pass-1: /pre-implement → /loop-spec → live-verify (human runs co-shipped script)
  Then Pass-2: /learning-extract → /ground-spec → wave-signoff
```

---

## 10. Coding-readiness unlock (PE — after plan on head)

Present this section in chat when the plan is persisted locally and Forge
readiness is filled. **No GitHub side effects** until PE completes the unlock
via authorized Forge / human actions.

| Item | Value |
|------|-------|
| Workflow outcome | `{outcome}` — {reason} |
| Verdict | GATE OPEN REQUEST / BLOCKED |
| Spec PR | {URL} |
| Spec PR head SHA | `{SHA}` |
| Gate label (current) | `spec-pending` |
| Gate label (target) | `spec-lgtm` |
| Local plan path | `{reports_dir}/{plan_prefix}-{initiative}.md` |
| Forge readiness | fill `handoff.forge` for `/commit-workspace` — do not commit inside this skill |
| Blocking items | none / {reason} |

Provision labels when missing:

```bash
launchpad apply-gates --repo <name> --apply
```

PE actions (all on **exact current head**):

1. Remove `spec-pending`, `spec-blocked`, `spec-revised`, `spec-stale`; add **`spec-lgtm`**
2. Submit GitHub **Approve** with attestation body (below)
3. Mark Draft PR **Ready for review**
4. Authorize merge (human or policy); then **`/create-board-tickets`** from §9

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

> **Primary:** `/create-board-tickets` creates **one GitHub Issue per wave** (`W0`, `W1`, …)
> from this section after spec merge. Wave bodies **must list every `TASK-*`**
> with exit criteria for human traceability (TASK sub-issues optional).
>
> Before creation, run `gh auth status` and search existing issues by initiative
> plus wave id. With explicit developer authorization, create only missing
> issues. If `gh` is unavailable, output exact commands and stop.
>
> Wave `id` must be exactly `W0`, `W1`, … — one issue per wave, not per TASK row.
> Each TASK **implements** one or more product `REQ-*` (never invent `REQ-W*`).
> Contract: `../../../references/workmanifest-contract.md` (`prayog/v1`).
> Ids: `../../../references/id-conventions.md`.
> Validate: `python scripts/workmanifest_contract.py` on this plan (P16 /
> `workmanifest-contract-pass`).
> Set `target.org` from governance and `target.project` from
> `governance.project_board.name` (read-only meta). Resolve with
> `launchpad board-bind --client <id>` — do not free-text board names.
>
> Do **not** put board `status`, observed evidence, or runtime head/SHA in this
> approved manifest — those live on the board and in Live-Verify / Wave-Execution
> artifacts.

```yaml
# Generated by /spec-implementation-plan — {DATE}
# LOCAL — do not commit to prayog-skills upstream
apiVersion: prayog/v1
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
  labels:
    - {initiative-label}

epic:
  id: EPIC
  repo: {meta-repo or primary codebase repo}
  title: "[feature] {INITIATIVE} — {short title}"
  codebase: {repo}
  spec_path: {SPEC_PATH}
  verify_command: {live script under live_verify_dir — not make test}
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
    verify_command: {wave W0 live script under live_verify_dir}
    tasks:
      - id: TASK-W0-01
        implements: [REQ-01, REQ-02]
        depends_on: []
        files:
          - path: {repo-relative/exact/path.py}
            action: create
        exit:
          criteria:
            - "{observable engineering result}"
          proof:
            kind: command
            command: "{proving command}"
            expected: "{expected result}"
            evidence_expected: "Wave-Execution-{INITIATIVE}-W0.md § TASK-W0-01"
      - id: TASK-W0-02
        implements: [REQ-03]
        depends_on: [TASK-W0-01]
        files:
          - path: {live_verify_dir/verify_….py}
            action: create
        exit:
          criteria:
            - "{observable engineering result}"
          proof:
            kind: command
            command: "{live verify command}"
            expected: "{expected result}"
            evidence_expected: "Live-Verify-{INITIATIVE}-W0.md"
    verification:
      check: "{check_command}"
      unit: "{test_command}"
      live:
        applicable: true
        mode: smoke
        command: {wave W0 live script under live_verify_dir}
        covers: [REQ-01, REQ-02]
        prerequisites:
          - "{env up / secrets present}"
        safe_test_data:
          - "{synthetic ids — no prod mutation}"
        steps:
          - "Run live verify script"
        expected_observations:
          - "{observable pass signal}"
        evidence_expected: "Live-Verify-{INITIATIVE}-W0.md"
        cleanup:
          - "{remove synthetic data}"
        stop_conditions:
          - "Non-zero exit or unexpected 5xx → stop; do not start Pass-2"
    body: |
      ## Wave goal

      {GOAL-W0 from spec}

      ## Tasks (from plan §2) — stable ids for loop-spec / board

      | Task | Implements | Depends on | Exit criteria | Proof |
      |------|------------|------------|---------------|-------|
      | TASK-W0-01 | REQ-01, REQ-02 | — | {exit} | {kind}/{command} |
      | TASK-W0-02 | REQ-03 | TASK-W0-01 | {exit} | {kind}/{command} |

      ## Done when

      - [ ] All W0 tasks complete per plan exit proof

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
    verify_command: {wave W1 live script under live_verify_dir — or N/A — reason}
    tasks:
      - id: TASK-W1-01
        implements: [REQ-{nn}]
        depends_on: []
        files:
          - path: {repo-relative/path}
            action: modify
        exit:
          criteria:
            - "{observable engineering result}"
          proof:
            kind: command
            command: "{proving command}"
            expected: "{expected result}"
            evidence_expected: "Wave-Execution-{INITIATIVE}-W1.md § TASK-W1-01"
    verification:
      check: "{check_command}"
      unit: "{test_command}"
      live:
        applicable: false
        reason: "{docs-only / no new product surface — P15 N/A}"
    body: |
      ## Wave goal

      {GOAL-W1 from spec}

      ## Tasks (from plan §2) — stable ids for loop-spec / board

      | Task | Implements | Depends on | Exit criteria | Proof |
      |------|------------|------------|---------------|-------|
      | TASK-W1-01 | REQ-{nn} | — | {exit} | {kind}/{command} |

      ## Done when

      - [ ] All W1 tasks complete per plan exit proof

      ## Spec reference

      {SPEC_PATH}

  # (one work: entry per wave — NOT one per TASK row; tasks[] + verification + body table required)
```
