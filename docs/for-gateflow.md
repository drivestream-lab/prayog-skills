# For Gateflow

Orientation for orchestrator / AgentRunner maintainers. Pin SSOT:
[`../workflow.yaml`](../workflow.yaml), [`../delivery-contract.yaml`](../delivery-contract.yaml),
[`../references/handoff-envelope.md`](../references/handoff-envelope.md),
[`../references/forge-side-effects.md`](../references/forge-side-effects.md).

## Hard rules

1. **No laptop overlay** — consume the remounted pin only.
2. **No skill-id allowlists** — read `dispatch` and `outcomes` from the pin.
3. **Same legality** as human invoke (`invocation-mode-is-not-an-exemption`).
4. Auto-dispatch a skill **only** when `dispatch: orchestrated` and programme
   trigger + handoff authorize.
5. On `type: human-checkpoint` or `external-action` — **STOP** (auth / human).
6. After a content hop: apply `forge.commit_workspace` / next `external-action`
   via **ForgeClient** — never auto-run `skills/forge/*`.
7. **WorkManifest contract** — before remounting a pin that expects
   `prayog/v1`, consume the **exact pinned** Prayog contract
   (`references/workmanifest-contract.md` + `scripts/workmanifest_contract.py`).
   Reject unsupported `apiVersion` / `kind` pairs fail-closed. Do not invent a
   Gateflow-local manifest schema.

## Pass-1 / Pass-2 (implement lane)

```text
PASS 1 — Enter-at pre-implement (continuous walk)
  pre-implement → loop-spec → wave-pr-action → live-verify
       live-verify.pass → wave-awaiting-closeout   # terminal park

PASS 2 — separate walk (API Enter-at learning-extract)
  learning-extract → ground-spec → wave-signoff
```

| Do | Don't |
|----|--------|
| After `pre-implement`, ForgeClient `commit_workspace` (checklist on `head_ref`) then continue to `loop-spec` | STOP / authorize `open_draft_pr` between pre-implement and loop-spec |
| After `loop-spec`, ForgeClient `commit_workspace` (code) then STOP on `wave-pr-action` | Auto-merge or invent a merge Forge action |
| Open Draft PR only via ForgeClient at `wave-pr-action` (checklist+code already on tip) | PR-at-start before skills / duplicate open |
| Stop after authorize at `live-verify` | Auto-run `verify` / `ground-spec` / `learning-extract` on Pass-1 |
| Treat unit/`make test` green as agent bar only | Treat unit green as live bar or skip human script run |
| Expect human to run co-shipped `live_verify_dir` script at `live-verify` | Auto-dispatch `/verify` on Pass-1 |
| Validate §9 via pinned WorkManifest contract before board seed / coding | Accept unsupported manifest versions or mutate approved intent at runtime |
| Require reviewed head SHA + human merge SHA at `wave-signoff.pass` | Let Gateflow/Forge merge the wave PR |
| Start closeout with Enter-at `learning-extract` | Treat `live-verify.pass` as resume into closeout skills (no authorize-resume in this slice) |
| Ingest Learning-Extract artifact / baton into DB (INIT-007) | Require the skill to HTTP POST as success |

`verify` is `dispatch: manual` — optional freeform path into `learning-extract`.
Unit green ≠ live prove; human runs the planned live script at `live-verify`.
BoardService / ForgeClient **project** epic/wave/task summaries onto the board;
board text is not a second WorkManifest authority.

## Checkpoint ids (breaking vs older pins)

| Old | New |
|-----|-----|
| `gate-1` | `prd-impact-acceptance` |
| `gate-2` | `coding-readiness` |
| `wave-human-decision` | `wave-signoff` |

`review_roles` keys on the contract match the **new** ids. Labels unchanged.

## Handoff / baton

- Skills dual-write `handoff:` to the workspace artifact and to bound
  `handoff_path` when present.
- `human_checkpoint: true` **iff** resolved next node `type` is
  `human-checkpoint` — not “artifact deserves review.”
- Learning payload: `{reports_dir}/Learning-Extract-{INIT}-W{N}.md` with
  markdown + fenced `learning_extract:` YAML (`L-*`). Worker ingest; skill does
  not own Postgres.

## Migration / remount

Development-stage outcome rubrics, T12, `GF-*` / G1–G10, WorkManifest
`prayog/v1` consumer alignment, `wave-pr-action`, and Forge-boundary cleanup
land only when programmes remount a new pin tag. Open initiatives keep their
prior pinned behavior until an explicit remount; migrated initiatives rerun from
the earliest materially affected stage. On remount, reject unsupported
WorkManifest versions and consume the exact pinned contract before BoardService
/ ForgeClient seed or walk.

Content skills still fill `handoff.forge` only — they never commit, push,
branch, open PRs, apply labels, or create board issues. Gateflow must STOP on
`wave-pr-action` and must **not** merge at `wave-signoff`.

## Out of scope (Initiative C2 — deferred)

Do **not** claim these as implemented on this remount:

- Evidence probes inside `initiative-feasibility` (need disposable env,
  ledger, timeout, cleanup)
- Blocking security-gate / T13 (needs coordinated pin + tenant role + reviewer
  evidence contracts)
- Task-level `parallel_safe` / concurrency / resource locks
- Branch cleanup / `delete_branch` Forge action

## Partner handoff

Share [for-gateflow.md](for-gateflow.md) when the pin is tagged/remounted.
Closeout Enter-at + learning DB ingest remain Gateflow INIT work.
