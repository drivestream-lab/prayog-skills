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
5. On `type: human-checkpoint` — **STOP** (human). On `type: external-action`
   — honor pin `authorization` (`explicit` ⇒ STOP then Forge; `automated` ⇒
   ForgeClient when requires complete, no interactive STOP).
6. After a content hop: apply `forge.commit_workspace` / next `external-action`
   via **ForgeClient** — never auto-run `skills/forge/*`.
7. **WorkManifest contract** — before remounting a pin that expects
   `prayog/v1`, consume the **exact pinned** Prayog contract
   (`references/workmanifest-contract.md` + `scripts/workmanifest_contract.py`).
   Reject unsupported `apiVersion` / `kind` pairs fail-closed. Do not invent a
   Gateflow-local manifest schema.
8. **`authorization` on every external-action** — required `explicit` |
   `automated`. Missing/unknown → fail closed. Day-one: `spec-pr-action`,
   `wave-pr-action`, `initiative-closure-pr-action-app`, and
   `initiative-closure-pr-action-meta` are `automated`; others `explicit`.

## Initiative closure lane

```text
initiative-closure (human)
  → purge-initiative-artifacts-app
  → initiative-closure-pr-action-app (automated) → initiative-closure-signoff-app
  → purge-initiative-artifacts-meta
  → initiative-closure-pr-action-meta (automated) → initiative-closure-signoff-meta
  → workflow-complete
```

Each lane is **self-contained:** purge → commit → open Draft PR → human merge.

| Do | Don't |
|----|--------|
| Enter-at / orch after `initiative-closure.pass` | Purge per `wave-signoff` |
| Bind **app** for eng loop; **meta** for PM loop | Invent a Gateflow-only delete path; couple skill packages to each other |
| Allowlist delete only; refuse KEEP; **handoff-only** (no `Purge-*.md`) | Authorize-before-delete STOP on purge skills; write new reports under `reports/` |
| `commit_workspace: required` on purge; automated `open_draft_pr` per repo | Merge via Forge at signoff |
| Treat board + product-spec H1–H4 as long-term identity after purge | Fail closed on missing feas/TDD/plan digests post-purge |
| Mid-lane freshness = product-spec H1–H3 + tip (light) | Mid-lane digest theatre as staleness SSOT |

Purge once for **both** repos after **all** waves (eng loop then PM loop).
Launchpad materializes the two purge skills; Gateflow implements Enter-at /
per-repo PR open on remount — not inside skill packages.

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
| After `loop-spec`, ForgeClient `commit_workspace` (code) then resolve `wave-pr-action` | Auto-merge or invent a merge Forge action |
| `wave-pr-action` is `authorization: automated` — ForgeClient `open_draft_pr` **without** interactive STOP when requires complete | Wait for human `/forge/authorize` on wave/spec Draft PR when pin says automated |
| First Draft PR view has checklist + code already on tip | PR-at-start before skills / duplicate open |
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

## Spec Pass-1 (spec lane)

```text
PASS 1 — Enter-at spec-draft (continuous walk until human stop)
  spec-draft → spec-pr-action (automated Draft PR)
       → initiative-feasibility
            pass|findings → spec-technical-review
                         → technical-review-approval  # human-checkpoint ⇒ STOP

Human after stop: agree REQs/ADRs on the Draft Spec PR → run
spec-implementation-plan (manual) → coding-readiness → explicit spec-merge / board
→ implement Enter-at.
```

| Do | Don't |
|----|--------|
| `POST /api/v1/waves/spec/start` with orchestrated `start_node` (default `spec-draft`) | Treat `spec-draft` as manual or overlay `dispatch` in Gateflow |
| Dual-bind `workspace` (app) + `meta_workspace` (meta checkout) into packaged prompts | Invent bind vars or omit meta on spec start |
| Fail closed when spec start meta checkout is missing/empty (**Gateflow**); packages declare `meta_workspace` optional in the shared schema SSOT | Require `meta_workspace: required: true` only on orch skills without a PE Decision (breaks shared-dict CI / implement binds) |
| After `spec-draft`, ForgeClient `commit_workspace` then automated `spec-pr-action` | Wait for `/forge/authorize` on Draft Spec PR when pin says automated |
| After feasibility, always continue to `spec-technical-review` (`pass` and `findings`) | Skip TDD on clean feasibility / auto-dispatch `spec-implementation-plan` |
| STOP at `technical-review-approval` (then human plan) | Orchestrate coding-readiness / `spec-merge` / board |
| Pass-2 closeout is **lane-agnostic** — Enter-at `learning-extract` on the wave/spec PR; skills do not HTTP to Gateflow | Build a spec-only closeout API shape in skills |

Orchestrated spec skills on this pin: `spec-draft`, `initiative-feasibility`,
`spec-technical-review`. Keep `spec-implementation-plan` manual and all Gate 2
/ merge nodes human or `authorization: explicit`.

**`meta_workspace` sharpness:** prompt schemas mark the var optional so
implement/PM packages stay honest when Gateflow does not bind meta. Spec-lane
Enter-at still **must** supply a non-empty meta checkout — that fail-closed
belongs to Gateflow `POST /waves/spec/start` / bind, not a per-package
`required: true` divergence from the shared dictionary.
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
`prayog/v1` consumer alignment, `wave-pr-action`, Forge-boundary cleanup, and
**Spec Pass-1** (`spec-draft` / `initiative-feasibility` /
`spec-technical-review` orchestrated + dual-bind `meta_workspace`) land only
when programmes remount this pin tip. Open initiatives keep their prior pinned
behavior until an explicit remount; migrated initiatives rerun from the
earliest materially affected stage. On remount, reject unsupported
WorkManifest versions and consume the exact pinned contract before BoardService
/ ForgeClient seed or walk.

**Remount checklist:** harness `.harness-pin.yaml` `agent_skills.ref` **must
equal** the consumed prayog-skills submodule SHA (or immutable tag tip). Do
**not** laptop-overlay `workflow.yaml`. After remount, Gateflow
`require_orchestrated_skill("spec-draft")` must succeed and
`POST /waves/spec/start` is legal for Spec Pass-1.

Content skills still fill `handoff.forge` only — they never commit, push,
branch, open PRs, apply labels, or create board issues. On remount, Gateflow
must honor `authorization` (automated Draft PR open on `spec-pr-action` /
`wave-pr-action` / `initiative-closure-pr-action-app` /
`initiative-closure-pr-action-meta`) and must **not** merge at `wave-signoff`
or `initiative-closure-signoff-app` / `initiative-closure-signoff-meta`.

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
Pass-2 closeout Enter-at (`learning-extract`) and learning ingest are owned by
Gateflow (lane-agnostic on wave/spec PR); skills only dual-write the baton —
they do not HTTP to Gateflow.