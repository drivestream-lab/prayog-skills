---
name: loop-spec
description: >-
  Execute the per-wave implementation loop: implement against spec, run
  verification, fix failures, repeat until green — then stop and request
  human checkpoint. Use during active wave development. Stops at human
  checkpoint; does not advance to the next wave.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, src/**
background_eligible: true
background_trigger: "wave issue moved to In Progress on board"
---

# Loop spec

Execute the per-wave loop:

```
implement → verify → fix → repeat → human checkpoint
```

## NON-NEGOTIABLE

1. Implement against the product spec only — do not implement scope from
   the next wave.
2. After each task, run `{check_command}` and `{test_command}` from the
   harness profile (or `tests_readme`). Both must pass before committing.
3. Fix failures before moving to the next task — do not accumulate failures.
4. When all tasks are green: stop and request **human checkpoint** via
   `/ground-spec`. Do not self-approve.
5. Do not skip verification steps to save time — failures caught here are
   cheaper than failures caught in `/ground-spec` or the wave PR review.

## Inputs

- Wave slice spec — from plan wave section (`docs/specification/reports/Implementation-Plan-{initiative}.md W{N}`)
- Pre-implement checklist — produced by `/pre-implement` for this wave
- `{check_command}` — static checks (from harness profile or `AGENTS.md`)
- `{test_command}` — unit verification (from harness profile or `tests_readme`)
- `{ground_command}` — spec ground check (optional; from harness profile if defined)

## Loop body (each task iteration)

1. Implement or fix the current task against the spec only.
2. Run `{check_command}` — zero warnings/errors required.
3. Run `{test_command}` — all tests pass required.
4. If any failure: fix and repeat from step 2.
5. When task is green: commit and move to next task.
6. After all tasks green: run `{ground_command}` if defined.
7. When everything is green: stop and hand off to `/ground-spec`.

## Stop conditions

- All wave tasks complete
- `{check_command}` exits 0
- `{test_command}` exits 0
- `{ground_command}` exits 0 (if defined)
- Human explicitly approves → `/ground-spec` runs → as-built status updated

## Chain position

```
/pre-implement (checklist produced)
    ↓
/loop-spec              ← YOU ARE HERE
  implement task → verify → fix → repeat
  human never sees intermediate failures
    ↓
  all green
    ↓
/ground-spec (validates wave against spec FRs, produces §Contracts produced)
```

## Usage with /loop timer (optional)

```
/loop 15m loop-spec: implement W{N} tasks in order per plan,
run {check_command} and {test_command} after each task,
fix failures before moving on, stop when all tasks green.
```
