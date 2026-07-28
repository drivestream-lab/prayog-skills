---
name: board-seed
description: >-
  After spec PR merge, produce board-seed readiness from Implementation Plan §9
  WorkManifest (EPIC + wave plan, board binding, dedupe notes). Fill
  handoff.forge for create_board_tickets. Create tickets via
  /create-board-tickets or orchestrator BoardService — not inside this skill.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/reports/**, .harness/profile.yaml
metadata:
  background_eligible: false
---

# Board seed

Produce **board readiness** for **one initiative tree** on the **programme
engineering board** after the spec package is merged. Applies to **any app
stack** — not `meta-pm`.

**Do not run before spec merge.** **Do not write product code.** **Do not
create board tickets in this skill** — recommend `/create-board-tickets`.

## NON-NEGOTIABLE

1. Resolve layout from `.harness/profile.yaml` or
   [references/layout-defaults.md](references/layout-defaults.md).
2. **Spec merge gate first** — merged `Implementation-Plan-{initiative}.md` on
   integration branch (`develop` or profile equivalent); closed spec PR had
   `spec-lgtm` on merge head when verifiable.
3. **Board binding** — resolve programme board from **read-only meta** governance:
   `{workspace}/{meta_repo}/config/governance-*.yaml` → `project_board.name`
   (exact match). If missing, run `launchpad board-bind --client <id>` and stop.
   Governance **wins** over plan §9 `target.project` free text.
4. Parse §9 WorkManifest YAML from the merged plan. Require `epic`, `work[]`
   with wave ids `W0`, `W1`, …. Each wave must list `tasks[]` (or an equivalent
   TASK table in `body`) with stable `TASK-*` ids and `implements: [REQ-…]`.
5. **Idempotent readiness** — search existing issues when tooling allows; record
   create vs existing in the readiness artifact for `/create-board-tickets`.
6. **Hierarchy plan** — EPIC first, then each wave as sub-issue on the same org
   Project. Initiative label on every issue. Wave bodies retain the TASK table.
7. **No forge / board mutations in this skill.** Fill `handoff.forge` with
   `action: create_board_tickets` and recommend `/create-board-tickets` after
   explicit authorization. See `../../../references/forge-side-effects.md#content-producers`.
8. If board tooling is unavailable, readiness + exact command examples in the
   output template are still valid — do not claim `seeded`.
9. Ids follow `../../../references/id-conventions.md`. Artifact paths follow
   `../../../references/artifact-write-contract.md`.

## Inputs

1. **Initiative id** — (REQUIRED) e.g. `INIT-MOBBOT-001`
2. **Integration branch** — (REQUIRED) default `develop`
3. **Merged plan** — `{reports_dir}/{plan_prefix}-{initiative}.md` §9
4. **Meta governance** — (REQUIRED) sibling meta clone:
   `../{meta_repo}/config/governance-<org>.yaml` or path from `clients.yaml`

## Prerequisite

- Spec PR **merged**; plan §9 on integration branch
- P14-valid WorkManifest in §9
- Programme board configured (`project_board.enabled` + `name`)

## Process

1. **T0 Gather** — initiative, plan path, §9 YAML, governance board binding,
   current repo slug, integration branch HEAD
2. **T1 Verify merge gate** — plan file exists; optional closed spec PR with
   `spec-lgtm`; stop if open spec branch context
3. **T2 Dedupe search** (read-only when tooling allows) — existing issues by
   initiative label
4. **T3 Present seed plan** — EPIC + waves, board name/URL, create vs existing,
   readiness fields for `/create-board-tickets` (example CLI may appear in
   [references/output-template.md](references/output-template.md) — examples only)
5. **T4 Hand off** — durable readiness + `handoff.forge`; recommend
   `/create-board-tickets` after user authorizes. Do not execute creates here.
6. **T5 Report** — readiness verdict (`ready` / `blocked`); never claim
   `seeded` until the forge skill / BoardService has run

## Output

Present seed readiness using [references/output-template.md](references/output-template.md).
Run checks from [references/checks.md](references/checks.md).

## Workflow handoff

1. Append/emit the envelope from `../../../references/handoff-envelope.md`. Use stage `board-seed`. Honor workflow `requires` on this node (SSOT).
2. When the invocation binds `handoff_path` (orchestrator / AgentRunner baton), also **overwrite** that path with the same `handoff:` envelope before exit. Leaving the baton empty is a failed stage for automated consumers. `artifact.path` remains the workspace skill output, not the baton path. See `../../../references/handoff-envelope.md` (Orchestrator baton).
3. Derive `next_candidates`, `human_checkpoint`, and `external_action` from pinned root `workflow.yaml` for `(stage: board-seed, outcome)` per `../../../references/handoff-envelope.md` (**Derive from pinned workflow**). Set `human_checkpoint: true` only when the resolved next node's `type` is `human-checkpoint` — never because the artifact "should be reviewed."
4. On readiness `pass`/`ready`, fill `handoff.forge` with `action: create_board_tickets` and instance slots from §9. Recommend `/create-board-tickets`. Follow `../../../references/forge-side-effects.md#content-producers`.
5. Pin `forge.commit_workspace: disabled` — board create is not a git commit hop.


**Transitions:** pinned root `workflow.yaml` for this stage (SSOT). Human or
agent may run this skill; legality and auto-dispatch follow `dispatch` +
delivery contract + latest handoff. `pass` typically advances to
`pre-implement` (orchestrated wave entry) after tickets exist via forge skill
or orchestrator.

Record seed status in `signals` (`ready` vs `seeded`). `next_candidates` never
authorize invoke. Board mutations need `/create-board-tickets` or ForgeClient.
