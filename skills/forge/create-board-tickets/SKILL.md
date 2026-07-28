---
name: create-board-tickets
description: >-
  Create board epic/wave tickets from board-seed readiness in handoff.forge
  (human walker). Orchestrators use BoardService / ForgeClient instead — do not
  auto-invoke this skill.
disable-model-invocation: true
---

# Create board tickets

Human-walker equivalent of Gateflow board / issue create
(`forge.action: create_board_tickets`).

## NON-NEGOTIABLE

1. Content skill (`board-seed`) owns **what** to create. This skill only
   **mutates** the board from complete readiness + `handoff.forge`.
2. Do not invent epic/TASK ids or bodies — read the durable board-seed
   artifact and handoff slots.
3. Dedupe before create when tooling allows; prefer update over duplicate.
4. Never apply approval labels (`*-lgtm`).
5. Explicit human authorization before create.
6. Tool-neutral (`gh issue`, project APIs, …) — examples only.

## Inputs

1. `board-seed` artifact + `handoff.forge` with `action: create_board_tickets`
2. Repo / project identifiers from harness profile or readiness
3. Optional existing issue search results

## Process

1. Validate readiness completeness.
2. Create or update epic and wave issues per plan.
3. Link sub-issues / project fields when the board model requires it.
4. Emit forge-step handoff with created ids in `signals`.

## Workflow handoff

1. Append/emit envelope; stage id: `create-board-tickets`.
2. Dual-write `handoff_path` when bound.
3. Not a graph node — continue from content `board-seed` transitions after
   tickets exist.
