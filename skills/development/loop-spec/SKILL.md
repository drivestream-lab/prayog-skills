---
name: loop-spec
description: >-
  Execute the per-wave implementation loop: implement against spec, run
  verification, fix failures, repeat until green — then stop and request
  human checkpoint. Use during active wave development. Stops at human
  checkpoint; does not advance to the next wave.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, src/**
metadata:
  background_eligible: true
  background_trigger: "wave issue moved to In Progress on board"
---

# Loop spec

Execute the per-wave loop:

```
implement → check/test → fix → repeat → live verify (when applicable)
→ ground report → human checkpoint
```

## NON-NEGOTIABLE

1. Implement against the product spec only — do not implement scope from
   the next wave.
2. **Prerequisites** — run only after `/pre-implement` produced a checklist
   with gate verdict PASS on the current wave. Do not run on an open Draft spec
   PR branch (`chore/*-spec-*`). The implementation plan must exist on
   `develop` (spec package merged with `spec-lgtm` on merge head).
3. After each task, run `{check_command}` and `{test_command}` from the
   harness profile (or `tests_readme`). Both must pass before committing.
4. Fix failures before moving to the next task — do not accumulate failures.
5. When all tasks are green: hand off to `/ground-spec`. The Ground Report is
   produced **before** the human checkpoint. Do not request or record human
   approval before grounding evidence exists, and do not self-approve.
6. Do not skip verification steps to save time — failures caught here are
   cheaper than failures caught in `/ground-spec` or the wave PR review.

## Inputs

- Wave slice spec — from plan wave section (`docs/specification/reports/Implementation-Plan-{initiative}.md W{N}`)
- Pre-implement checklist — produced by `/pre-implement` for this wave
- `{check_command}` — static checks (from harness profile or `AGENTS.md`)
- `{test_command}` — unit verification (from harness profile or `tests_readme`)
- `{verify_command}` — live verification (when applicable; from the plan and `tests_readme`)
- `{ground_command}` — automated input to `/ground-spec` (optional; from harness profile if defined)

## Loop body (each task iteration)

1. Implement or fix the current task against the spec only.
2. Run `{check_command}` — zero warnings/errors required.
3. Run `{test_command}` — all tests pass required.
4. If any failure: fix and repeat from step 2.
5. When task is green: commit and move to next task.
6. After all tasks are green, run `{verify_command}` when the plan marks live
   verification applicable; fix failures and repeat.
7. Stop and hand off to `/ground-spec`; that skill runs `{ground_command}` when
   defined and produces the Ground Report.

## Stop conditions

- All wave tasks complete
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
  implement task → verify → fix → repeat
  human never sees intermediate failures
    ↓
  checks/tests/live verify green
    ↓
/ground-spec (validates wave against spec FRs, produces §Contracts produced)
    ↓
  human checkpoint → as-built human_approved → merge
```

## Usage with /loop timer (optional)

```
/loop 15m loop-spec: implement W{N} tasks in order per plan,
run {check_command} and {test_command} after each task,
fix failures before moving on, stop when all tasks green.
```

## Workflow handoff

Emit the envelope from `../../../references/handoff-envelope.md` in the final
task summary and persist the same state in the wave tracker/commits. Use stage
`loop-spec`.

**Transitions:** pinned root `workflow.yaml` for this stage (SSOT). Human or
agent may run this skill; orchestrators may auto-dispatch when authorized.
Same legality for both invoke paths.

List failed commands/tasks under `blockers`; do not advance while any remain.
`next_candidates` never authorize invoke.
