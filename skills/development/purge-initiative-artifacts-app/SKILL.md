---
name: purge-initiative-artifacts-app
description: >-
  After initiative-closure judgment, delete allowlisted app working papers for
  one initiative (feas, TDD, plan, per-wave reports, Draft ADRs). Refuse KEEP
  paths (product INIT, Accepted ADRs, source/tests/verify scripts). Part of the
  initiative-closure lane from develop; commit via Forge. No authorize-before-
  delete — safety is allowlist + refuse KEEP. Use Enter-at or
  /purge-initiative-artifacts-app after all waves are done.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, .harness/profile.yaml
metadata:
  background_eligible: true
  background_trigger: "initiative-closure.pass — purge app working papers"
---

# Purge initiative artifacts (app)

Delete **PURGE-set** files under the **app** repo for one initiative after all
waves are done. **Do not** delete durable KEEP roots. Git history remains the
archive.

Normative allowlist / refuse:
[`../../../references/artifact-write-contract.md`](../../../references/artifact-write-contract.md).

## NON-NEGOTIABLE

1. Resolve layout from `.harness/profile.yaml` or
   [references/layout-defaults.md](references/layout-defaults.md).
2. Require initiative id `INIT-*`. Scope deletes to that initiative only.
3. Delete **only** the app PURGE allowlist when present:
   - `{reports_dir}/Initiative-Feasibility-Report-{INIT}.md`
   - `{reports_dir}/Technical-Review-{INIT}.md`
   - `{reports_dir}/Implementation-Plan-{INIT}.md`
   - `{reports_dir}/Pre-Implement-{INIT}-W*.md`
   - `{reports_dir}/Wave-Execution-{INIT}-W*.md`
   - `{reports_dir}/Live-Verify-{INIT}-W*.md`
   - `{reports_dir}/Ground-Report-*-W*.md` for this initiative/spec
   - `{reports_dir}/Learning-Extract-{INIT}-W*.md`
   - `{adr_dir}/adr-*-*.md` that are still **Draft** (not Accepted)
4. **Refuse** (never delete): `{product_spec_dir}/INIT-*.md` for this
   initiative; **Accepted** ADRs; anything under `source_roots`,
   `unit_tests_dir`, `live_verify_dir` **scripts**; `.harness/`; product source.
5. Idempotent: missing allowlisted files → ok. Empty delete set → still `pass`
   with rationale.
6. Work on the **initiative-closure** head cut from integration (`develop`)
   when bound; do not invent a branch. Fill `handoff.forge` for
   `commit_workspace` when pin requires commit. Do **not** open the closure PR
   here — that is `initiative-closure-pr-action`.
7. No Gateflow authorize-before-delete. No merge. Never apply `*-lgtm`.
8. Write a short purge note under `{reports_dir}/Purge-App-{INIT}.md` listing
   `deleted`, `missing_ok`, `refused`, then handoff. (The purge note itself may
   be left for the human or included on the closure tip — do not add it to a
   recursive purge of itself in the same run after writing.)
9. Dual-walker: same procedure for human `/purge-initiative-artifacts-app` and
   Gateflow orch.

## Inputs

1. **Initiative id** — (REQUIRED)
2. **Workspace** — app repo root (REQUIRED)
3. **Layout** — profile or layout-defaults
4. **Handoff baton** — when `handoff_path` bound

## Process

1. **T0** — resolve INIT, reports_dir, adr_dir, product_spec_dir; build candidate
   list from allowlist globs.
2. **T1** — classify each path: delete / missing_ok / refused (if somehow KEEP).
3. **T2** — delete delete-set only.
4. **T3** — write purge note + handoff (`stage: purge-initiative-artifacts-app`).
5. **T4** — fill `handoff.forge` for `commit_workspace` when pin expects it.

## Outcome selection

| Outcome | When | Next (from workflow) |
|---------|------|----------------------|
| `pass` | Allowlist processed; no KEEP deleted; purge note written | `purge-initiative-artifacts-meta` |
| `needs-input` | Initiative id or layout unreadable | `initiative-closure` |
| `blocked` | Attempt would touch KEEP; refuse and stop | `initiative-closure` |
| `failed` | Delete/IO error on otherwise valid allowlist | `initiative-closure` |

## Output

Use [references/output-template.md](references/output-template.md).
Checks: [references/checks.md](references/checks.md).

## Workflow handoff

1. Append/emit envelope from `../../../references/handoff-envelope.md`. Stage
   `purge-initiative-artifacts-app`.
2. When `handoff_path` is bound, **overwrite** that path with the same
   `handoff:` envelope before exit.
3. Derive `next_candidates` and `human_checkpoint` from pinned `workflow.yaml`
   for `(stage: purge-initiative-artifacts-app, outcome)`. Set
   `human_checkpoint: true` only when the resolved next node's `type` is
   `human-checkpoint`.
4. Happy path: `outcome: pass` → next `purge-initiative-artifacts-meta` →
   `human_checkpoint: false`.
5. Follow `../../../references/forge-side-effects.md#content-producers` when pin
   `forge.commit_workspace` is not `disabled`.
