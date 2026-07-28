---
name: create-board-tickets
description: >-
  After spec PR merge, seed the programme engineering board from Implementation
  Plan §9 WorkManifest: verify merge gate and board binding, present the EPIC/wave
  plan, then after explicit authorization create epic and wave issues. Human
  walker ForgeClient parity (create_board_tickets). Orchestrators use
  BoardService / ForgeClient on board-tickets-action — do not auto-invoke.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/reports/**, .harness/profile.yaml
---

# Create board tickets

Human-walker equivalent of Gateflow **board create**
(`forge.action: create_board_tickets`).

**One command after merge:** read plan §9 → preflight → confirm → create.
There is no separate `/board-seed` content skill. WorkManifest already lives in
the implementation plan.

**Do not run before spec merge.** **Do not write product code.**

## NON-NEGOTIABLE

1. Resolve layout from `.harness/profile.yaml` or
   [references/layout-defaults.md](references/layout-defaults.md).
2. **Spec merge gate first** — merged `Implementation-Plan-{initiative}.md` on
   integration branch; closed spec PR had `spec-lgtm` on merge head when
   verifiable.
3. **Board binding** — resolve programme board from **read-only meta** governance:
   `{workspace}/{meta_repo}/config/governance-*.yaml` → `project_board.name`.
   If missing, run `launchpad board-bind --client <id>` and stop. Governance
   **wins** over plan §9 `target.project` free text.
4. Parse §9 WorkManifest YAML. Require `epic`, `work[]` with wave ids `W0`,
   `W1`, …. Each wave must list `tasks[]` (or TASK table in `body`) with stable
   `TASK-*` ids and `implements: [REQ-…]`.
5. **Idempotent** — search existing issues by initiative label; create only
   missing items; link existing waves under EPIC when parent missing.
6. **Hierarchy** — EPIC first, then each wave as sub-issue on the same org
   Project. Initiative label on every issue. Wave bodies retain the TASK table.
7. **Explicit authorization before mutate.** Present the seed plan; create only
   after the human confirms.
8. Never apply approval labels (`*-lgtm`). Tool-neutral Forge tooling (`gh`,
   project APIs, …) — examples only.
9. If tooling unavailable, print exact commands from
   [references/output-template.md](references/output-template.md) and stop —
   do not claim `seeded`.
10. Ids: `../../../references/id-conventions.md`. Paths:
    `../../../references/artifact-write-contract.md`.

## Inputs

1. **Initiative id** — (REQUIRED)
2. **Integration branch** — (REQUIRED) default `develop`
3. **Merged plan** — `{reports_dir}/{plan_prefix}-{initiative}.md` §9
4. **Meta governance** — (REQUIRED) sibling meta clone /
   `governance-<org>.yaml`

## Prerequisite

- Spec PR **merged**; P14-valid WorkManifest in §9
- Programme board configured (`project_board.enabled` + `name`)
- Pin next step: `board-tickets-action` (`forge.action: create_board_tickets`)

## Process

1. **T0 Gather** — initiative, plan path, §9 YAML, governance board, repo slug,
   integration HEAD
2. **T1 Verify merge gate** — plan on integration; optional closed spec PR with
   `spec-lgtm`; stop if still on open spec branch
3. **T2 Dedupe search** — existing issues by initiative label (read-only)
4. **T3 Present seed plan** — EPIC + waves, board name/URL, create vs existing;
   ask for authorization
5. **T4 Execute** (authorized only) — create/update EPIC and waves; project
   links / sub-issues per board model
6. **T5 Report** — issue URLs; `signals.seeded` / `already-seeded`; handoff

Use [references/output-template.md](references/output-template.md) and
[references/checks.md](references/checks.md).

## Workflow handoff

1. Append/emit envelope from `../../../references/handoff-envelope.md`. Stage id
   for this forge skill note: `create-board-tickets` (not a graph node).
2. Dual-write `handoff_path` when bound.
3. After successful seed, programme continues at `pre-implement` per pin
   (`board-tickets-action` `pass` → `pre-implement`). Do not invent graph edges.
4. Honor pin `requires` on `board-tickets-action` (spec merged, plan current,
   WorkManifest P14).
