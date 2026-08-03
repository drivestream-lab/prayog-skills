---
name: purge-initiative-artifacts-meta
description: >-
  After app purge in the initiative-closure lane, delete allowlisted meta PM
  working papers (Validation-Report, Resolution) for one initiative. Refuse KEEP
  paths (PRD, Impact-Map). Commit via Forge on meta closure head from develop.
  No authorize-before-delete. Use Enter-at or /purge-initiative-artifacts-meta
  after purge-initiative-artifacts-app.
disable-model-invocation: true
paths: prd/**, .harness/profile.yaml
metadata:
  background_eligible: true
  background_trigger: "purge-initiative-artifacts-app.pass — purge meta working papers"
---

# Purge initiative artifacts (meta)

Delete **PURGE-set** files under the **meta** repo for one initiative after all
waves are done (and after app purge in the pin lane). **Do not** delete durable
KEEP roots.

Normative allowlist / refuse:
[`../../../references/artifact-write-contract.md`](../../../references/artifact-write-contract.md).

## NON-NEGOTIABLE

1. Resolve layout from `.harness/profile.yaml` or
   [references/layout-defaults.md](references/layout-defaults.md).
2. Require initiative id `INIT-*`. Scope deletes to that initiative only.
3. Delete **only** when present:
   - `{reports_dir}/Validation-Report-{INIT}.md`
   - `{reports_dir}/Resolution-{INIT}.md`
4. **Refuse** (never delete): `prd/INIT-*.md` for this initiative;
   `{reports_dir}/Impact-Map-{INIT}.md`; service catalog; governance.
5. Idempotent: missing allowlisted files → ok.
6. Workspace is the **meta** checkout (Gateflow binds meta root; human runs in
   meta clone). Fill `handoff.forge` for `commit_workspace` when pin requires
   it. Do **not** open the closure PR here —
   `initiative-closure-pr-action` follows.
7. No Gateflow authorize-before-delete. No merge. Never apply `*-lgtm`.
8. Write `{reports_dir}/Purge-Meta-{INIT}.md` with deleted / missing_ok / refused.
9. Dual-walker parity with human `/purge-initiative-artifacts-meta`.

## Inputs

1. **Initiative id** — (REQUIRED)
2. **Workspace** — meta repo root (REQUIRED)
3. **Layout** — profile or layout-defaults
4. **Handoff baton** — when `handoff_path` bound

## Process

1. **T0** — resolve INIT and reports_dir; list allowlist candidates.
2. **T1** — classify delete / missing_ok / refused.
3. **T2** — delete delete-set only.
4. **T3** — write purge note + handoff (`stage: purge-initiative-artifacts-meta`).
5. **T4** — fill `handoff.forge` for `commit_workspace` and readiness for
   `open_draft_pr` when next is `initiative-closure-pr-action`.

## Outcome selection

| Outcome | When | Next (from workflow) |
|---------|------|----------------------|
| `pass` | Allowlist processed; no KEEP deleted | `initiative-closure-pr-action` |
| `needs-input` | Initiative id or layout unreadable | `initiative-closure` |
| `blocked` | Attempt would touch KEEP | `initiative-closure` |
| `failed` | Delete/IO error | `initiative-closure` |

On `pass`, fill `handoff.forge` for `open_draft_pr` when the pin routes to
`initiative-closure-pr-action` (title/body_path for closure PR).

## Output

Use [references/output-template.md](references/output-template.md).
Checks: [references/checks.md](references/checks.md).

## Workflow handoff

1. Append/emit envelope from `../../../references/handoff-envelope.md`. Stage
   `purge-initiative-artifacts-meta`.
2. When `handoff_path` is bound, **overwrite** that path with the same
   `handoff:` envelope before exit.
3. Derive `next_candidates`, `human_checkpoint`, and `external_action` from
   pinned `workflow.yaml` for `(stage: purge-initiative-artifacts-meta, outcome)`.
   Set `human_checkpoint: true` only when the resolved next node's `type` is
   `human-checkpoint`.
4. Happy path: `outcome: pass` → next `initiative-closure-pr-action` →
   `human_checkpoint: false`, `external_action: true`. Fill `handoff.forge` for
   `open_draft_pr` per pin `requires`.
5. Follow `../../../references/forge-side-effects.md#content-producers` when pin
   `forge.commit_workspace` is not `disabled` or next is an external-action.
