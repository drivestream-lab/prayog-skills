---
name: verify
description: >-
  Define or run live verify discipline for a feature — one live-verify artifact
  per product area, no overlap with unit tests. Use when finishing a slice, adding
  live-verify tests, or when asked what command proves the feature on a running stack.
disable-model-invocation: true
paths: AGENTS.md, tests/**, docs/specification/as-built/**
---

# Verify

Clarify **live verify** vs **unit** for one feature, or run verify when a human
asks. This skill is an **optional manual aid** (`dispatch: manual`) — not on the
Pass-1 edge. The Pass-1 gate after `/loop-spec` is human-checkpoint
`live-verify` (human runs the co-shipped script from the plan).

Read `AGENTS.md`, `tests_readme`, and `rules_glob` (include testing-verify rule when present). Policy: [references/verify-policy.md](references/verify-policy.md). Paths: `.harness/profile.yaml` or [references/layout-defaults.md](../pre-implement/references/layout-defaults.md).

## Rules

Resolve `unit_tests_dir`, `live_verify_dir`, `debug_tests_dir` from profile.

| Layer | Who runs | Location (profile key) | Proves |
|-------|----------|------------------------|--------|
| Unit | Agent (`/loop-spec`) | `unit_tests_dir` | Logic, branches, edge cases |
| Live verify | Human (`live-verify`) | `live_verify_dir` | Product feature on **running** stack |
| Debug | Exploratory | `debug_tests_dir` | Exploration — not gating |

**Co-ship:** new/material product surfaces ship the live script in the same wave
as the code (plan P15). `/loop-spec` delivers the FILE; it does not run live
verify as success.

**No overlap:** do not assert the same behavior in unit and live verify for the same feature.

## Toolchain vs live verify

Commands come from `tests_readme` and profile toolchain — do not hardcode stack-specific commands in the skill.

Do not skip prerequisites (running server, config files, bootstrap scripts) documented in `tests_readme`.

Live `verify_command` is not `{test_command}` / unit-only.

## Output format (plan mode)

```markdown
## Verify plan — FEATURE

### Unit scope
- What to test in {unit_tests_dir} (no live stack)

### Verify script
- Path: {live_verify_dir}/...
- Prerequisites: (from tests_readme)
- Command: ...
- Pass criteria: exit 0, expected shape / behavior

### As-built row
- Update implementation-status.md: unit-tested / live-verified

### Overlap check
- Confirm no duplicate assertions vs unit
```

## Run mode

If the user asks to **run** verify: state the exact command from `tests_readme` and tracker **Verify command**; run it when the environment is available; report pass/fail.

## Workflow handoff

1. Emit the envelope from `../../../references/handoff-envelope.md` in the verify result and persist the command/evidence in the tracker or report. Use stage `verify`.
2. When the invocation binds `handoff_path` (orchestrator / AgentRunner baton), also **overwrite** that path with the same `handoff:` envelope before exit. Leaving the baton empty is a failed stage for automated consumers. `artifact.path` remains the workspace skill output, not the baton path. See `../../../references/handoff-envelope.md` (Orchestrator baton).
3. Derive `next_candidates` and `human_checkpoint` from pinned root `workflow.yaml` for `(stage: verify, outcome)` per `../../../references/handoff-envelope.md` (**Derive from pinned workflow**). Set `human_checkpoint: true` only when the resolved next node's `type` is `human-checkpoint` — never because the artifact "should be reviewed."
4. Happy path: `outcome: pass` or `skipped` → next `learning-extract` (`type: skill`) → `human_checkpoint: false`.


4. Follow `../../../references/forge-side-effects.md#content-producers` when this stage's pin has `forge.commit_workspace` other than `disabled` or next is an `external-action` with `forge.requires` — fill `handoff.forge` / recommend the matching `/forge` skill; do not treat local CLI as skill success.


**Transitions:** pinned root `workflow.yaml` for this stage (SSOT). Human or
agent may run this skill; orchestrators must **not** auto-dispatch
(`dispatch: manual`). Same legality for human invoke paths.

Never mark `pass` without command output or equivalent reproducible evidence.
`next_candidates` never authorize invoke.
