---
name: loop-spec
description: >-
  Execute the per-wave implementation loop: implement against spec one TASK at
  a time, run checks/tests, fix failures, repeat until green — then stop for
  human live-verify. Binds each iteration to TASK-* + board wave issue. Use
  during active wave development. Does not run ground-spec or learning-extract.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, src/**
metadata:
  background_eligible: true
  background_trigger: "wave issue moved to In Progress on board"
---

# Loop spec

Execute the per-wave Pass-1 loop:

```
implement TASK → check/test → fix → repeat
→ stop at live-verify (human prove + patch tip)
```

Closeout (`/learning-extract` → `/ground-spec`) is a **separate** Pass-2 after
human live-verify — not this skill's job.

Conventions: `../../../references/id-conventions.md`.

## NON-NEGOTIABLE

1. Implement against the product spec only — do not implement scope from
   the next wave.
2. **Prerequisites** — run only after `/pre-implement` produced a checklist
   with gate verdict PASS on the current wave. Do not run on an open Draft spec
   PR branch (`chore/*-spec-*`). The implementation plan must exist on
   `develop` (spec package merged with `spec-lgtm` on merge head).
3. After each **TASK**, run `{check_command}` and `{test_command}` from the
   harness profile (or `tests_readme`). Both must pass before committing.
4. Fix failures before moving to the next TASK — do not accumulate failures.
5. When all TASKs are green: **stop** for human checkpoint `live-verify`. Do
   **not** run `/ground-spec` or `/learning-extract` in this hop. Do not
   self-approve the wave.
6. Do not skip check/test steps to save time.
7. **Bind execution** — each iteration names `TASK-W{n}-{nn}`, the wave board
   issue URL/number, and `implements: [REQ-…]` from the plan / wave body.
8. **Structured failures** — on check/test failure, record under handoff
   `blockers` the `TASK-*` id plus command and short why; comment the same on
   the wave issue when Forge tooling is available and authorized. Do not advance
   while any TASK blocker remains.

## Inputs

- Wave slice — plan wave section (`Implementation-Plan-{initiative}.md` W{N})
  including TASK table with **Implements** `REQ-*`
- Board wave issue — URL/number from `/create-board-tickets` / pre-implement checklist
- Pre-implement checklist — produced by `/pre-implement` for this wave
- `{check_command}` — static checks (from harness profile or `AGENTS.md`)
- `{test_command}` — unit verification (from harness profile or `tests_readme`)
- `{verify_command}` — documented for the **human** live-verify stop (not run as
  success criteria of this skill)

## Loop body (each TASK iteration)

1. Announce current binding: `TASK-*`, wave issue, `REQ-*` implements, done-when.
2. Implement or fix the current TASK against the spec only.
3. Run `{check_command}` — zero warnings/errors required.
4. Run `{test_command}` — all tests pass required.
5. If any failure: fix and repeat from step 3; keep `TASK-*` in `blockers` with
   `{command, expected, actual/summary}` until green.
6. When TASK is green: commit (message cites `TASK-*`), clear that blocker, move
   to next TASK.
7. After all TASKs are green: hand off with `pass` → pin next `live-verify`
   (human prove + patch). Optional: note applicable `{verify_command}` for the
   human — do not treat running it as this skill's success.

## Stop conditions

- All wave TASKs complete
- `{check_command}` exits 0
- `{test_command}` exits 0
- Handoff `pass` toward `live-verify`

## Chain position

Illustrative only — **transitions SSOT:** pinned root `workflow.yaml`
(`dispatch: orchestrated` on this node).

```
/pre-implement (checklist produced)
    ↓
/loop-spec              ← YOU ARE HERE
  bind TASK + wave issue → implement → check/test → fix → repeat
  failures: handoff blockers + optional issue comment (TASK-*, why)
    ↓
  checks/tests green
    ↓
live-verify (human prove + patch tip) → wave-awaiting-closeout
    ↓ (Pass-2 Enter-at or /learning-extract)
/learning-extract → /ground-spec → wave-signoff
```

## Usage with /loop timer (optional)

```
/loop 15m loop-spec: implement W{N} TASK-* in order per plan,
run {check_command} and {test_command} after each TASK,
fix failures before moving on, stop when all TASKs green.
```

## Workflow handoff

1. Emit the envelope from `../../../references/handoff-envelope.md` in the final task summary and persist the same state in the wave tracker/commits. Use stage `loop-spec`.
2. When the invocation binds `handoff_path` (orchestrator / AgentRunner baton), also **overwrite** that path with the same `handoff:` envelope before exit. Leaving the baton empty is a failed stage for automated consumers. `artifact.path` remains the workspace skill output, not the baton path. See `../../../references/handoff-envelope.md` (Orchestrator baton).
3. Derive `next_candidates` and `human_checkpoint` from pinned root `workflow.yaml` for `(stage: loop-spec, outcome)` per `../../../references/handoff-envelope.md` (**Derive from pinned workflow**). Set `human_checkpoint: true` only when the resolved next node's `type` is `human-checkpoint` — never because the artifact "should be reviewed."
4. Happy path: `outcome: pass` → next `live-verify` (`type: human-checkpoint`) → `human_checkpoint: true`.


4. Follow `../../../references/forge-side-effects.md#content-producers` when this stage's pin has `forge.commit_workspace` other than `disabled` or next is an `external-action` with `forge.requires` — fill `handoff.forge` / recommend the matching `/forge` skill; do not treat local CLI as skill success.


**Transitions:** pinned root `workflow.yaml` for this stage (SSOT). Human or
agent may run this skill; orchestrators may auto-dispatch when authorized.
Same legality for both invoke paths.

List failed `TASK-*` (and command/why) under `blockers`; do not advance while
any remain. `signals` SHOULD include `wave_issue`, `current_task`, and
`implements`. `next_candidates` never authorize invoke.
