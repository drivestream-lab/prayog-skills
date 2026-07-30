---
name: pre-implement
description: >-
  Before implementing one wave slice, produce a pre-flight checklist: verify
  the prior wave's human gate is satisfied, confirm contracts consumed from
  prior Ground Reports match what was actually built, then read specs/ADRs/rules.
  Gate-only — never opens a branch or implements product code. Use when starting
  a wave, checking readiness for /loop-spec, or asked what to read before coding.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, .cursor/rules/**
metadata:
  background_eligible: true
  background_trigger: "wave issue moved to In Progress on board"
---

# Pre-implement

Produce the **pre-flight checklist** for one wave slice. This skill is
**gate-only**: it never opens a branch and never implements product code —
even if the user asks after the checklist. Implementation belongs to
`/loop-spec`. Content skills write locally and emit Forge readiness; they do
not commit, push, branch, open PRs, label, create issues, or merge.

Canonical artifact:
`{reports_dir}/Pre-Implement-{INIT}-W{N}.md`
([`../../../references/artifact-write-contract.md`](../../../references/artifact-write-contract.md)).

## NON-NEGOTIABLE

1. Resolve paths from `.harness/profile.yaml` when present; else
   [references/layout-defaults.md](references/layout-defaults.md).
2. **Gate check first** — before reading anything else, confirm the prior
   wave's Ground Report exists and its as-built row is `human_approved`.
   If not: stop and state which gate is unsatisfied. Do not produce a
   checklist for a wave whose predecessor is not approved.
3. Read `rules_glob` per the domain-filter approach in
   [references/governance.md](references/governance.md) — not all files.
4. Read relevant ADRs (keyword-match, then deep-read matched Accepted ADRs).
5. **Never implement product code** and **never open/create a branch**. Output
   the checklist (+ Forge readiness when board/branch readiness is absent).
6. Cite concrete file paths for this repo and slice.
7. Describe contracts in engineering terms — entry points, input/output shapes,
   invariants. Do not use language-specific syntax.
8. Verify the plan's source-freshness table is CURRENT and its impact-map
   revision/scope digest still match the canonical handoff. Stop on stale input.
9. Resolve `check_command` and `test_command`. Resolve `verify_command` as the
   **live** script under `live_verify_dir` when the wave plan triggers P15
   (new/material product surface) — **FAIL** the gate on bare N/A or
   unit-only (`make test` / `{test_command}`). Resolve `ground_command` when
   applicable. If the plan/profile/`AGENTS.md`/`tests_readme` cannot supply a
   required command, stop with MISSING command. The human runs
   `{verify_command}` at checkpoint `live-verify`; this skill does not execute it.
10. **Canonical WorkManifest** — consume plan §9 (`prayog/v1` `WorkManifest`)
    as the execution-intent authority (see
    [`../../../references/workmanifest-contract.md`](../../../references/workmanifest-contract.md)).
    Run `scripts/workmanifest_contract.py` (or import `validate_workmanifest`)
    against the merged plan / §9 YAML. **Fail closed** (`blocked` or `failed`)
    when any of the following hold for this wave:
    - contract check fails (`workmanifest-contract-pass` false);
    - any `TASK-*` lacks complete `exit.criteria` + `exit.proof`
      (kind/command|review/expected/evidence_expected);
    - P15 applies and the wave lacks a live-verification contract (`verification.live`
      applicable with script under `live_verify_dir`) or unit-as-live command.
    Do **not** treat board issue text as a second authority — project TASK ids /
    REQ mappings / exit summaries from the manifest into the checklist.
11. Confirm board seed from plan §9: **EPIC** issue exists, every declared wave
    issue exists, and waves are **sub-issues of the EPIC** on the programme
    board (governance `project_board.name`). Board/branch/PR state is
    **read-only**. If seed or bound wave head is missing/partial: stop, emit
    Forge / external-action readiness (e.g. recommend `/create-board-tickets`
    or wave-head binding) — **do not** invoke mutation from this skill.
12. **Spec merge gate** — before W0 (and before any `/loop-spec`), confirm:
    - bound wave head context is the **integration branch** (`develop`) or a
      `feature/INIT-*-w{N}-*` wave branch cut from it — **not** an open
      `chore/*-spec-*` Draft spec PR branch (wave head is bound by Forge/human
      context — this skill does not open it);
    - `docs/specification/reports/Implementation-Plan-{initiative}.md` exists on
      the integration branch (spec PR was merged);
    - the merged spec PR head carried **`spec-lgtm`** (verify via `gh pr view`
      on the closed spec PR: label present and `mergeCommit`/`headRefOid`
      matches attestation or Approve `commit_id`);
    - board tickets seeded (wave issues exist per rule 11).
    If any check fails: stop — do not produce a pass checklist or write product
    code.

## Outcome selection

Map evidence to delivery outcomes only (pinned `workflow.yaml`):

| Outcome | When |
|---------|------|
| `pass` | Gate verdict PASS; WorkManifest contract clean for this wave; preflight artifact written; commands resolved; board seeded; prior wave approved (or W0 plan PE sign-off); wave head bound in Forge/human context |
| `needs-input` | Authoritative source absent/unreadable (plan, Ground Report, commands, profile, §9 YAML) so readiness cannot be determined |
| `blocked` | Authoritative source exists and shows an unsatisfied gate (WorkManifest contract fail, TASK missing exit proof, missing/applicable live-verify contract when P15 applies, prior wave not `human_approved`, board seed missing/partial, open Draft spec branch) |
| `stale` | Plan source-freshness not CURRENT, or impact-map revision/scope digest mismatch |
| `failed` | Execution error while reading inputs, running the WorkManifest validator, or writing the preflight artifact |

When board/branch readiness is absent: prefer `blocked` (or `needs-input` if
authority cannot be read) and fill `handoff.forge` / recommend the matching
forge skill — never create the branch or tickets here.

Happy path: `pass` → `loop-spec` (no PR STOP here). On `pass`, fill
`handoff.forge` for **`commit_workspace`** so Forge publishes
`Pre-Implement-{INIT}-W{N}.md` onto the bound `head_ref` before coding.
Draft PR open happens later at `wave-pr-action` (after `loop-spec`).

## Chain position

Illustrative only — **transitions SSOT:** pinned root `workflow.yaml`
(`dispatch: orchestrated` on this node). Procedure gates below still apply.

```
spec merge (spec-lgtm on head) → board seed (Forge) → wave issue In Progress
    ↓
/ground-spec (prior wave) → human_approved in as-built   [Wn>0 only]
    ↓
/pre-implement               ← YOU ARE HERE (gate-only)
  gate: spec merged + board seeded + prior wave human_approved?
  reads: Ground-Report-W{N-1}.md §Contracts produced
  produces: Pre-Implement-{INIT}-W{N}.md
    ↓
  Forge commit_workspace (checklist on head_ref) → /loop-spec
    ↓
  Forge commit_workspace (code) → wave-pr-action (open_draft_pr)
    ↓
  live-verify (human on Draft PR) → closeout: /learning-extract → /ground-spec
```

**Do not run on an open Draft spec PR branch** (`chore/*-spec-*`). Coding
starts only after the spec package is merged to `develop` and a wave head is
bound outside this skill.

## Read order

1. **Source and gate check** — spec merge gate (rule 12); plan on integration
   branch; plan sources CURRENT; impact-map scope current; **WorkManifest
   contract pass** for this wave (rule 10); canonical commands resolved; board
   issues exist (read-only); `as-built/implementation-status.md` prior wave =
   `human_approved` (Wn>0)? If any answer is no: stop with the matching outcome
   + Forge readiness when mutation is required elsewhere.
2. **Contracts consumed** — `reports/Ground-Report-W{N-1}.md` §Contracts
   produced: for each contract this wave depends on, read the entry point,
   input shape, output shape, and invariants as verified by the prior Ground
   Report. Confirm against actual source (scan `source_roots`) — not against
   spec alone.
3. `AGENTS.md` — constitution pin, verify commands, process links
4. **Domain-filtered MDC rules** — per [references/governance.md](references/governance.md)
5. **Relevant ADRs** — keyword-match slice scope; read matched Accepted ADRs
6. Initiative / slice spec — path from tracker Spec path or plan wave section
7. Plan wave section / §9 WorkManifest — `reports/Implementation-Plan-{initiative}.md`
   W{N}: carry forward source digests, command contract, MDC notes, ADR notes,
   and from the **canonical WorkManifest** for this wave: **TASK ids**,
   `depends_on`, file scope, **Implements `REQ-*`**, exit criteria/proof, and
   wave `verification` (check/unit/live). Cite the board wave issue URL and
   list every `TASK-*` for this wave in the checklist (projection only).
8. `tests_readme` — when the slice adds or changes verification

**Gate for W0 (first wave):** no prior Ground Report exists. The gate is
the implementation plan PE sign-off (§0 of the plan). Confirm it is marked
complete before producing the W0 checklist.

**Cross-service / cross-module:** when this slice calls a module from another
service or a prior wave that has NOT yet been grounded, flag it explicitly in
the checklist under "Unconfirmed contracts" — do not silently assume the
interface.

## Output format

Write `{reports_dir}/Pre-Implement-{INIT}-W{N}.md` using
[references/output-template.md](references/output-template.md). Fill
concrete paths for this repo and slice.

## Workflow handoff

1. Append/emit the envelope from `../../../references/handoff-envelope.md` to the checklist output. Use stage `pre-implement`.
2. When the invocation binds `handoff_path` (orchestrator / AgentRunner baton), also **overwrite** that path with the same `handoff:` envelope before exit. Leaving the baton empty is a failed stage for automated consumers. `artifact.path` remains the workspace skill output, not the baton path. See `../../../references/handoff-envelope.md` (Orchestrator baton).
3. Derive `next_candidates`, `human_checkpoint`, and `external_action` from pinned root `workflow.yaml` for `(stage: pre-implement, outcome)` per `../../../references/handoff-envelope.md` (**Derive from pinned workflow**). Set `human_checkpoint: true` only when the resolved next node's `type` is `human-checkpoint` — never because the artifact "should be reviewed." Set `external_action: true` only when next is `external-action`.
4. Happy path: `outcome: pass` → next `loop-spec` (`type: skill`) → `human_checkpoint: false`, `external_action: false`. Pin has `forge.commit_workspace: required` — fill `handoff.forge` for `commit_workspace` so Forge publishes the Pre-Implement artifact onto the bound wave head before `/loop-spec`. Do **not** open the Draft PR here.


5. Follow `../../../references/forge-side-effects.md#content-producers` when this stage's pin has `forge.commit_workspace` other than `disabled` or next is an `external-action` with `forge.requires` — fill `handoff.forge` / recommend the matching `/forge` skill; do not treat local CLI as skill success.


**Transitions:** pinned root `workflow.yaml` for this stage (SSOT). Human or
agent may run this skill; orchestrators may auto-dispatch when
`dispatch: orchestrated` and trigger + handoff authorize. Same legality rules
for both invoke paths.

Record the board issue URL/id, wave `TASK-*` list, and resolved command
contract in `signals`. `next_candidates` never authorize invoke.
