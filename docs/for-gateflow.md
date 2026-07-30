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

## Pass-1 / Pass-2 (implement lane)

```text
PASS 1 — Enter-at pre-implement (continuous walk)
  pre-implement → loop-spec → live-verify
       live-verify.pass → wave-awaiting-closeout   # terminal park

PASS 2 — separate walk (API Enter-at learning-extract)
  learning-extract → ground-spec → wave-signoff
```

| Do | Don't |
|----|--------|
| Stop after `loop-spec` at `live-verify` | Auto-run `verify` / `ground-spec` / `learning-extract` on Pass-1 |
| Treat unit/`make test` green as agent bar only | Treat unit green as live bar or skip human script run |
| Expect human to run co-shipped `live_verify_dir` script at `live-verify` | Auto-dispatch `/verify` on Pass-1 |
| Start closeout with Enter-at `learning-extract` | Treat `live-verify.pass` as resume into closeout skills (no authorize-resume in this slice) |
| Ingest Learning-Extract artifact / baton into DB (INIT-007) | Require the skill to HTTP POST as success |

`verify` is `dispatch: manual` — optional freeform path into `learning-extract`.
Unit green ≠ live prove; human runs the planned live script at `live-verify`.

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

## Partner handoff

Share [for-gateflow.md](for-gateflow.md) when the pin is tagged/remounted.
Closeout Enter-at + learning DB ingest remain Gateflow INIT work.
