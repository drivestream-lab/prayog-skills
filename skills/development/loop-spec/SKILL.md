---
name: loop-spec
description: >-
  Execute the per-wave implementation loop: implement against spec one TASK at
  a time, run verification, fix failures, repeat until green — then stop and
  request human checkpoint. Binds each iteration to TASK-* + board wave issue.
  Use during active wave development. Stops at human checkpoint; does not
  advance to the next wave.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, src/**
metadata:
  background_eligible: true
  background_trigger: "wave issue moved to In Progress on board"
---

# Loop spec

Execute the per-wave loop:

```
implement TASK → check/test → fix → repeat → live verify (when applicable)
→ ground report → human checkpoint
```

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
5. When all TASKs are green: hand off to `/ground-spec`. The Ground Report is
   produced **before** the human checkpoint. Do not request or record human
   approval before grounding evidence exists, and do not self-approve.
6. Do not skip verification steps to save time — failures caught here are
   cheaper than failures caught in `/ground-spec` or the wave PR review.
7. **Bind execution** — each iteration names `TASK-W{n}-{nn}`, the wave board
   issue URL/number, and `implements: [REQ-…]` from the plan / wave body.
8. **Structured failures** — on check/test/verify failure, record under handoff
   `blockers` the `TASK-*` id plus command and short why; comment the same on
   the wave issue when `gh` is available and authorized. Do not advance while
   any TASK blocker remains.

## Inputs

- Wave slice — plan wave section (`Implementation-Plan-{initiative}.md` W{N})
  including TASK table with **Implements** `REQ-*`
- Board wave issue — URL/number from `/board-seed` / pre-implement checklist
- Pre-implement checklist — produced by `/pre-implement` for this wave
- `{check_command}` — static checks (from harness profile or `AGENTS.md`)
- `{test_command}` — unit verification (from harness profile or `tests_readme`)
- `{verify_command}` — live verification (when applicable; from the plan and `tests_readme`)
- `{ground_command}` — automated input to `/ground-spec` (optional; from harness profile if defined)

## Loop body (each TASK iteration)

1. Announce current binding: `TASK-*`, wave issue, `REQ-*` implements, done-when.
2. Implement or fix the current TASK against the spec only.
3. Run `{check_command}` — zero warnings/errors required.
4. Run `{test_command}` — all tests pass required.
5. If any failure: fix and repeat from step 3; keep `TASK-*` in `blockers` with
   `{command, expected, actual/summary}` until green.
6. When TASK is green: commit (message cites `TASK-*`), clear that blocker, move
   to next TASK.
7. After all TASKs are green, run `{verify_command}` when the plan marks live
   verification applicable; fix failures and repeat.
8. Stop and hand off to `/ground-spec`; that skill runs `{ground_command}` when
   defined and produces the Ground Report.

## Stop conditions

- All wave TASKs complete
- `{check_command}` exits 0
- `{test_command}` exits 0
- `{verify_command}` exits 0 (when applicable)
- `/ground-spec` is the next action; human review happens only after its report
- Human approves Ground Report → as-built status updated → wave PR may merge

## Chain position

Illustrative only — **transitions SSOT:** pinned root `workflow.yaml`
(`dispatch: orchestrated` on this node).

```
/pre-implement (checklist produced)
    ↓
/loop-spec              ← YOU ARE HERE
  bind TASK + wave issue → implement → verify → fix → repeat
  failures: handoff blockers + optional issue comment (TASK-*, why)
    ↓
  checks/tests/live verify green
    ↓
/ground-spec (validates wave against spec REQs, produces §Contracts produced)
    ↓
  human checkpoint → as-built human_approved → merge
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


**Transitions:** pinned root `workflow.yaml` for this stage (SSOT). Human or
agent may run this skill; orchestrators may auto-dispatch when authorized.
Same legality for both invoke paths.

List failed `TASK-*` (and command/why) under `blockers`; do not advance while
any remain. `signals` SHOULD include `wave_issue`, `current_task`, and
`implements`. `next_candidates` never authorize invoke.
