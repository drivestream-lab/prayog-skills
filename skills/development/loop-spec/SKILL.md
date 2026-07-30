---
name: loop-spec
description: >-
  Execute the per-wave implementation loop: implement against spec one TASK at
  a time, run checks/tests, fix failures, record local TASK proof — then stop
  for human live-verify. Writes Wave-Execution artifact and one stage-level
  commit_workspace Forge package after the wave is green. Never commits/pushes.
  Use during active wave development. Does not run ground-spec or learning-extract.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, src/**
metadata:
  background_eligible: true
  background_trigger: "wave issue moved to In Progress on board"
---

# Loop spec

Execute the per-wave Pass-1 loop:

```
implement TASK → check/test → fix → record local proof → repeat
→ write Wave-Execution + Forge commit_workspace readiness
→ stop at live-verify (human prove + patch tip)
```

Closeout (`/learning-extract` → `/ground-spec`) is a **separate** Pass-2 after
human live-verify — not this skill's job.

Content skills write locally and emit Forge readiness; they do not commit,
push, branch, open PRs, label, create issues, or merge.

Conventions: `../../../references/id-conventions.md`,
`../../../references/artifact-write-contract.md`.

Canonical artifact after the wave is green:
`{reports_dir}/Wave-Execution-{INIT}-W{N}.md`.

## NON-NEGOTIABLE

1. Implement against the product spec only — do not implement scope from
   the next wave.
2. **Prerequisites** — run only after `/pre-implement` produced a checklist
   with gate verdict PASS on the current wave. Do not run on an open Draft spec
   PR branch (`chore/*-spec-*`). The implementation plan must exist on
   `develop` (spec package merged with `spec-lgtm` on merge head). Wave head
   is bound by Forge/human context. Canonical §9 WorkManifest
   (`prayog/v1`) must already have passed contract validation at pre-implement.
3. **Consume WorkManifest tasks** — execute `TASK-*` for this wave in
   **dependency order** (`depends_on` DAG within the wave). Remain within each
   TASK's declared `files[]` path/action scope. Do **not** mutate the approved
   WorkManifest intent (no rewriting exit criteria, deps, or live contract in
   §9). Persist **actual** command/evidence results only in
   `Wave-Execution-{INIT}-W{N}.md` and the stage handoff.
4. After each **TASK**, run `{check_command}` and `{test_command}` from the
   harness profile (or `tests_readme`) — **check/unit layers only**. Both must
   pass before recording the TASK complete. Implement live-verify **FILE**
   TASKs (scripts under `live_verify_dir`) when the plan/manifest includes
   them — deliver the planned artifact; do **not** execute live verify,
   `verify_all`, or `{verify_command}` as this skill's success bar, and
   **never claim** human smoke/sandbox success.
5. Fix failures before moving to the next TASK — do not accumulate failures.
6. When all TASKs are green: write `Wave-Execution-{INIT}-W{N}.md`, emit
   completed `TASK-*` IDs/evidence (observed commands + results), fill one
   stage-level `commit_workspace` Forge package, then **stop** for human
   checkpoint `live-verify`. Do **not** run `/ground-spec` or
   `/learning-extract` in this hop. Do not self-approve the wave. Handoff
   **MUST** list the human `{verify_command}` (co-shipped live script
   path/command).
7. Do not skip check/test steps to save time.
8. **Bind execution** — each iteration names `TASK-W{n}-{nn}`, the wave board
   issue URL/number, and `implements: [REQ-…]` from the **WorkManifest**
   (board body is projection only).
9. **Structured failures** — on check/test failure, record under handoff
   `blockers` the `TASK-*` id plus command and short why; prepare optional
   issue-comment Forge readiness when tooling is authorized elsewhere. Do not
   advance while any TASK blocker remains.
10. **Never commit or push** inside this skill — not per TASK and not at wave
    end. ForgeClient or `/commit-workspace` publishes the workspace tree to the
    bound wave head after this hop when the pin requires it.

## Outcome selection

| Outcome | When |
|---------|------|
| `pass` | All wave TASKs green; `Wave-Execution-*` written with completed TASK ids/evidence; `handoff.forge` filled for stage-level `commit_workspace`; handoff lists human `{verify_command}` |
| `findings` | Check/test failure on a TASK that needs further local fix (keep `TASK-*` in blockers) |
| `blocked` | Prerequisites fail or an authoritative gate prevents progress (e.g. missing pre-implement PASS, unbound wave head) |
| `failed` | Execution error running commands or writing the execution artifact |

Do **not** run human live verification or grounding. Do **not** emit `skipped`.

Happy path: `pass` → `live-verify`.

## Inputs

- Wave slice — plan §9 WorkManifest (`prayog/v1`) for W{N}: tasks with
  `depends_on`, `files[]`, `implements` `REQ-*`, exit proof, and wave
  `verification` (check/unit/live intent)
- Board wave issue — URL/number from board seed / pre-implement checklist
  (projection of manifest — not a second authority)
- Pre-implement checklist — `{reports_dir}/Pre-Implement-{INIT}-W{N}.md`
- `{check_command}` — static checks (from harness profile or `AGENTS.md`)
- `{test_command}` — unit verification (from harness profile or `tests_readme`)
- `{verify_command}` — **human** live-verify entry (script under `live_verify_dir`);
  document on handoff; **never** run as exit criteria of this skill

## Loop body (each TASK iteration)

1. Announce current binding: `TASK-*`, wave issue, `REQ-*` implements, file
   scope, done-when / exit proof **expected** (from WorkManifest).
2. Implement or fix the current TASK against the spec only — stay inside
   declared `files[]` scope.
3. Run `{check_command}` — zero warnings/errors required.
4. Run `{test_command}` — all tests pass required.
5. If any failure: fix and repeat from step 3; keep `TASK-*` in `blockers` with
   `{command, expected, actual/summary}` until green.
6. When TASK is green: **record local completion/proof** in Wave-Execution /
   handoff (actual commands + evidence, files touched, exit criteria met);
   clear that blocker; move to the next dependency-ready TASK. Do **not**
   commit. Do **not** edit the approved WorkManifest.
7. After all TASKs are green:
   - Write `{reports_dir}/Wave-Execution-{INIT}-W{N}.md` listing completed
     `TASK-*` ids and **observed** evidence (not mutated intent).
   - Fill one stage-level `handoff.forge` `commit_workspace` package
     (suggested message citing wave + TASK ids). ForgeClient or
     `/commit-workspace` publishes to the bound wave head.
   - Hand off with `pass` → pin next `live-verify`. Handoff **MUST** include
     `{verify_command}` for the human. Do **not** run live verify /
     `verify_all` / optional `/verify` as this skill's success, and do not
     claim smoke/sandbox human success.

## Wave-Execution artifact (minimum)

```markdown
# Wave execution — {INIT} W{N}

| Field | Value |
|-------|-------|
| Initiative | {INIT} |
| Wave | W{N} |
| Wave head context | Bound by Forge/human: `{ref}` |
| WorkManifest source | plan §9 (immutable intent — not mutated) |
| Outcome | pass / findings / blocked / failed |

## Completed TASKS
| TASK | Implements | Declared files | Proof expected (manifest) | Observed (command / evidence) | Status |
|------|------------|----------------|---------------------------|-------------------------------|--------|
| TASK-W{N}-01 | REQ-… | path… | exit.proof.expected | `{check}` / `{test}` + paths | green |

## Live verify (human — not claimed here)
- Planned script: `{verify_command}` under `live_verify_dir`
- Agent created planned FILE: yes/no — **did not** run smoke/sandbox as success

## Forge readiness
- action: commit_workspace
- message: [{INIT} W{N}] … — TASK-…
```

## Stop conditions

- All wave TASKs complete with local proof recorded
- `{check_command}` exits 0
- `{test_command}` exits 0
- `Wave-Execution-*` written; stage-level `commit_workspace` readiness filled
- Handoff `pass` toward `live-verify`

## Chain position

Illustrative only — **transitions SSOT:** pinned root `workflow.yaml`
(`dispatch: orchestrated` on this node).

```
/pre-implement (checklist PASS)
    ↓
/loop-spec              ← YOU ARE HERE
  bind WorkManifest TASK + wave issue → implement in file scope
  → check/unit only → fix → record observed proof (do not mutate manifest)
  failures: handoff blockers (TASK-*, why); no commits
    ↓
  checks/tests green → Wave-Execution-* + commit_workspace readiness
    ↓
live-verify (human prove + patch tip) → wave-awaiting-closeout
    ↓ (Pass-2 Enter-at or /learning-extract)
/learning-extract → /ground-spec → wave-signoff
```

## Usage with /loop timer (optional)

```
/loop 15m loop-spec: implement W{N} TASK-* in WorkManifest dependency order,
stay in declared file scope, run {check_command} and {test_command} after each
TASK, record observed proof in Wave-Execution (do not mutate WorkManifest,
do not commit), fix failures before moving on, stop when all TASKs green.
```

## Workflow handoff

1. Emit the envelope from `../../../references/handoff-envelope.md` in the final task summary and persist state in `Wave-Execution-*`. Use stage `loop-spec`.
2. When the invocation binds `handoff_path` (orchestrator / AgentRunner baton), also **overwrite** that path with the same `handoff:` envelope before exit. Leaving the baton empty is a failed stage for automated consumers. `artifact.path` remains the workspace skill output, not the baton path. See `../../../references/handoff-envelope.md` (Orchestrator baton).
3. Derive `next_candidates` and `human_checkpoint` from pinned root `workflow.yaml` for `(stage: loop-spec, outcome)` per `../../../references/handoff-envelope.md` (**Derive from pinned workflow**). Set `human_checkpoint: true` only when the resolved next node's `type` is `human-checkpoint` — never because the artifact "should be reviewed."
4. Happy path: `outcome: pass` → next `live-verify` (`type: human-checkpoint`) → `human_checkpoint: true`.


4. Follow `../../../references/forge-side-effects.md#content-producers` when this stage's pin has `forge.commit_workspace` other than `disabled` or next is an `external-action` with `forge.requires` — fill `handoff.forge` / recommend the matching `/forge` skill; do not treat local CLI as skill success.


**Transitions:** pinned root `workflow.yaml` for this stage (SSOT). Human or
agent may run this skill; orchestrators may auto-dispatch when authorized.
Same legality for both invoke paths.

List failed `TASK-*` (and command/why) under `blockers`; do not advance while
any remain. `signals` SHOULD include `wave_issue`, `current_task`,
`implements`, and completed TASK ids. `next_candidates` never authorize invoke.
