---
name: verify
description: >-
  Define or run live verify discipline for a feature — one live-verify artifact
  per product area, no overlap with unit tests. Writes Live-Verify-{INIT}-W{N}.md
  with expected-versus-observed evidence. Use when finishing a slice, adding
  live-verify tests, or when asked what command proves the feature on a running stack.
disable-model-invocation: true
paths: AGENTS.md, tests/**, docs/specification/as-built/**
---

# Verify

Clarify **live verify** vs **unit** for one feature, or run verify when a human
asks. This skill is an **optional manual aid** (`dispatch: manual`) — not on the
Pass-1 edge. The Pass-1 gate after `/loop-spec` is human-checkpoint
`live-verify` (human runs the co-shipped script from the plan).

Command execution (running the live script) is **verification tooling**, not a
Forge mutation. Content skills still do not commit, push, open PRs, apply
labels, or update trackers — emit Forge readiness when the durable report needs
publication.

Canonical artifact:
`{reports_dir}/Live-Verify-{INIT}-W{N}.md`
([`../../../references/artifact-write-contract.md`](../../../references/artifact-write-contract.md)).

Read `AGENTS.md`, `tests_readme`, and `rules_glob` (include testing-verify rule when present). Policy: [references/verify-policy.md](references/verify-policy.md). Paths: `.harness/profile.yaml` or [references/layout-defaults.md](../pre-implement/references/layout-defaults.md).

## Rules

Resolve `unit_tests_dir`, `live_verify_dir`, `debug_tests_dir` from profile.

| Layer | Who runs | Location (profile key) | Proves |
|-------|----------|------------------------|--------|
| Unit | Agent (`/loop-spec`) | `unit_tests_dir` | Logic, branches, edge cases |
| Integration / contract | Agent or CI when harness defines it | Contract suite from `tests_readme` / profile | Cross-module wiring / interface shapes |
| Smoke | Human (`live-verify`) / optional `/verify` | `live_verify_dir` | Critical path on **running** stack |
| Sandbox | Human / optional `/verify` | `live_verify_dir` + sandbox env | Env-dependent behavior with safe test data |
| Debug | Exploratory | `debug_tests_dir` | Exploration — not gating |

Policy details: [references/verify-policy.md](references/verify-policy.md).

**Co-ship:** new/material product surfaces ship the live script in the same wave
as the code (plan P15). `/loop-spec` delivers the FILE; it does not run live
verify as success.

**No overlap / no unit-as-live:** do not assert the same behavior in unit and
live verify for the same feature. Do **not** duplicate unit-only assertions in
smoke/sandbox scripts. Live `verify_command` is never `{test_command}` /
`make test`.

**Expected-versus-observed:** every run writes human evidence comparing plan
expected observations to observed results (exit code + key output / UI).

**Bind at runtime:** record the actual environment class and build SHA / wave
head under test — do not invent them at plan time.

## Outcome selection

| Outcome | When |
|---------|------|
| `pass` | Live command (or plan-mode deliverable) succeeded; `Live-Verify-*` written with expected-versus-observed evidence; no open blockers |
| `skipped` | Live verify not applicable for this wave/feature (documented N/A reason); artifact records the skip |
| `findings` | Command ran and observed results miss expected observations (fixable product/script issues) |
| `blocked` | Prerequisites or environment prevent a meaningful run (server down, missing config/secrets, unsafe sandbox) |
| `failed` | Tool/execution error preventing a conclusive result |

Never commit evidence, update a PR/tracker, or apply labels. Fill
`handoff.forge` when report publication is needed.

Happy path: `pass` or `skipped` → `learning-extract`.

## Toolchain vs live verify

Commands come from `tests_readme` and profile toolchain — do not hardcode stack-specific commands in the skill.

Do not skip prerequisites (running server, config files, bootstrap scripts) documented in `tests_readme`.

Live `verify_command` is not `{test_command}` / unit-only.

## Output format (plan or run mode)

Write `{reports_dir}/Live-Verify-{INIT}-W{N}.md`:

```markdown
## Live verify — {INIT} W{N} — FEATURE

| Field | Value |
|-------|-------|
| Initiative | {INIT} |
| Wave | W{N} |
| Mode | plan / run |
| Environment | {sandbox / fuller stack / …} — bound at runtime |
| Build / head | `{sha or ref}` — bound at runtime |
| Outcome | pass / skipped / findings / blocked / failed |
| Outcome reason | {one sentence} |

### Unit scope
- What is covered in {unit_tests_dir} (no live stack) — for overlap check only

### Verify script
- Path: {live_verify_dir}/...
- Prerequisites: (from tests_readme)
- Command: ...
- Expected observations: ...
- Observed (run mode): ...
- Pass criteria: exit 0 + expected shape / behavior
- Cleanup / stop conditions: {mandatory when sandbox applies}

### Evidence
| Expected | Observed | Match? |
|----------|----------|--------|
| … | … | yes / no |

### Overlap check
- Confirm no duplicate assertions vs unit

### Forge readiness
- Publish Live-Verify report via commit_workspace when pin expects it — do not mutate PR/labels here
```

## Run mode

If the user asks to **run** verify: state the exact command from `tests_readme`
and tracker **Verify command**; bind environment + build; run it when the
environment is available; write expected-versus-observed evidence; select
outcome per the table above.

## Workflow handoff

1. Emit the envelope from `../../../references/handoff-envelope.md` in the verify result and persist command/evidence in `Live-Verify-*`. Use stage `verify`.
2. When the invocation binds `handoff_path` (orchestrator / AgentRunner baton), also **overwrite** that path with the same `handoff:` envelope before exit. Leaving the baton empty is a failed stage for automated consumers. `artifact.path` remains the workspace skill output, not the baton path. See `../../../references/handoff-envelope.md` (Orchestrator baton).
3. Derive `next_candidates` and `human_checkpoint` from pinned root `workflow.yaml` for `(stage: verify, outcome)` per `../../../references/handoff-envelope.md` (**Derive from pinned workflow**). Set `human_checkpoint: true` only when the resolved next node's `type` is `human-checkpoint` — never because the artifact "should be reviewed."
4. Happy path: `outcome: pass` or `skipped` → next `learning-extract` (`type: skill`) → `human_checkpoint: false`.


4. Follow `../../../references/forge-side-effects.md#content-producers` when this stage's pin has `forge.commit_workspace` other than `disabled` or next is an `external-action` with `forge.requires` — fill `handoff.forge` / recommend the matching `/forge` skill; do not treat local CLI as skill success.


**Transitions:** pinned root `workflow.yaml` for this stage (SSOT). Human or
agent may run this skill; orchestrators must **not** auto-dispatch
(`dispatch: manual`). Same legality for human invoke paths.

Never mark `pass` without command output or equivalent reproducible evidence
(plan mode may `pass` only when the plan artifact is complete and run is not
requested). `next_candidates` never authorize invoke.
