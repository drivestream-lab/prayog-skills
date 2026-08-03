# Overview — what prayog-skills is

prayog-skills is the **portable delivery pin** for specification-driven
development: a process graph, skill packages, and contracts that both humans
(Cursor `/skill`) and orchestrators (Gateflow) share.

It is **not** only “a folder of Cursor tips.” Remounted consumers get the same
legality rules whether a human or an AgentRunner runs a hop.

## Three surfaces

```text
workflow.yaml + delivery-contract.yaml
        │  pin: nodes, dispatch, forge, checkpoints
        ▼
skills/{requirements,development,forge}/
        │  procedures + prompt packages
        ▼
references/
        │  handoff, forge, prompts, ids, artifacts
```

| Surface | Owns |
|---------|------|
| **Pin** | Navigation, `dispatch` (`manual` \| `orchestrated`), `forge` policy, human-checkpoint `purpose` |
| **Skills** | How to produce artifacts; fill `handoff` / `handoff.forge`; never invent next hops |
| **References** | Field schemas and producer rules |

## Two walkers, one pin

| Walker | Runs skills | Publishes mutations |
|--------|-------------|---------------------|
| **Human** | `/skill` in IDE | Forge skills under `skills/forge/` after explicit auth |
| **Orchestrator** | Auto only if `dispatch: orchestrated` | ForgeClient / BoardService from pin ⋉ handoff |

Content skills do **not** treat local `gh` as automate success. See
[`../references/forge-side-effects.md`](../references/forge-side-effects.md).

## Two lanes (do not mix)

| Lane | Workspace | Profile skills |
|------|-----------|----------------|
| **PM** | `*-meta` | `requirements_skills` + `forge_skills` |
| **Dev** | App repos | `development_skills` + `forge_skills` |

## Implement lane — Pass-1 / Pass-2 (current pin)

```text
PASS 1 (orchestrated walk)
  pre-implement → loop-spec → wave-pr-action → live-verify
       → wave-awaiting-closeout               # park (not wave-complete)

PASS 2 (Enter-at learning-extract, or human /learning-extract)
  learning-extract → ground-spec → wave-signoff
```

- `pre-implement` is **gate-only** (read-only board/head checks). It never opens
  a wave branch or implements product code — that belongs to Forge + `loop-spec`.
  It consumes the canonical §9 WorkManifest (`prayog/v1`) and fails closed when
  the shared contract check fails, a TASK lacks exit proof, or an applicable
  wave lacks a live-verification contract/script.
  Pin has `commit_workspace: required` so Forge publishes `Pre-Implement-*` onto
  `head_ref` **before** coding (no Draft-PR STOP between pre-implement and loop).
- `loop-spec` executes WorkManifest tasks in dependency order within declared
  file scope; records observed proof in `Wave-Execution-*` / handoff without
  mutating approved manifest intent; runs check+unit only; creates planned live
  scripts but never claims human smoke/sandbox success. Emits `commit_workspace`
  readiness for code on the same `head_ref`.
- On `loop-spec.pass`, next is **`wave-pr-action`** (reuse `open_draft_pr` with
  `title` / `body_path` / `head_ref` / `base_ref`). Pin sets
  `authorization: automated` — ForgeClient opens the Draft PR without an
  interactive authorize STOP when requires are complete. First Draft PR view
  should already include checklist + code. There is **no** merge Forge action —
  merge stays human-only at `wave-signoff`. This placement avoids a mid-Pass-1
  STOP before coding (trade: no PR URL during coding).
  (`spec-pr-action` is also `automated`; other external-actions stay `explicit`.)
- `verify` is **manual** (optional aid) — not on the Pass-1 edge. Layer ownership
  covers unit, integration/contract, smoke, and sandbox; live evidence requires
  expected-versus-observed rows in `Live-Verify-{INIT}-W{N}.md` and must not
  duplicate unit-only assertions.
- `ground-spec` validates only WorkManifest-assigned wave REQs, uses **`GF-*`**
  findings (G1–G10), and never commits or merges. It prepares the exact-head
  human sign-off package (PR URL, reviewed head SHA, evidence refs).
- `wave-signoff.pass` is legal only after the human confirms the reviewed PR
  head, merges manually, and records the merge commit SHA.
- **Co-ship live verify:** when a wave adds/changes a product surface, the same
  wave ships the live script under `live_verify_dir` (plan P15). `/loop-spec`
  runs check+unit only; the human executes the script at `live-verify` before
  Pass-2 closeout automation continues.
- **WorkManifest authority (Initiative B):** Prayog owns `prayog/v1`. **Board**
  issues after seed are the long-term WorkManifest home; plan §9 is the
  walk-time carrier (may be purged at initiative closure). Stage artifacts
  project or record evidence — they are not a second execution-intent authority.
  Validator: `scripts/workmanifest_contract.py`; plan check P16; predicate
  `workmanifest-contract-pass`.
- **Durable identity:** H1–H4 (PRD digest, scope digest, map revision, product-
  spec citations) and G1–G3 (gate/merge SHAs). Mid-lane feas/TDD/plan digests are
  walk-time only — not long-term `stale` SSOT. See
  [`../references/artifact-write-contract.md`](../references/artifact-write-contract.md).
- Checkpoints use **purpose-named ids** (`prd-impact-acceptance`,
  `coding-readiness`, `live-verify`, `wave-signoff`, `initiative-closure`,
  `initiative-closure-signoff`). GitHub labels stay lane-named
  (`impact-map-*`, `spec-*`).

## Initiative closure lane (current pin)

After **all** waves are done (not per wave-signoff):

```text
initiative-closure (human judgment)
  → purge-initiative-artifacts-app    # app PURGE allowlist; commit_workspace required
  → purge-initiative-artifacts-meta   # meta PURGE allowlist; commit_workspace required
  → initiative-closure-pr-action      # open_draft_pr automated
  → initiative-closure-signoff        # human merge to develop
  → workflow-complete
```

One mental model: purge **everything** on the PURGE allowlist for app and meta
once. KEEP roots (PRD, Impact-Map, product INIT, Accepted ADRs, code/tests/
verify scripts) and board WM survive. No Gateflow authorize-before-delete;
safety is allowlist + refuse KEEP. No per-wave purge hop.

## Spec lane — Pass-1 (current pin)

```text
PASS 1 (orchestrated walk until human stop)
  spec-draft → spec-pr-action → initiative-feasibility
       pass|findings → spec-technical-review
                    → technical-review-approval   # human-checkpoint ⇒ STOP
  Human: spec-implementation-plan (manual) → coding-readiness → merge / board
```

Orchestrated: `spec-draft`, `initiative-feasibility`, `spec-technical-review`.
Feasibility always enters TDD (`pass` and `findings`). `spec-pr-action` is
`authorization: automated`. Plan / coding-readiness / `spec-merge` / board stay
human or explicit. Packaged prompts bind optional `meta_workspace`. See
[`for-gateflow.md`](for-gateflow.md#spec-pass-1-spec-lane).

## Design lane — ownership and outcomes

- **Spec** owns observable product behavior (`REQ-*`). Architecture questions are
  routed, not decided in the product spec.
- **Feasibility** is read-only triage: PE/ADR blockers → `findings`; missing
  PM/domain answers → `needs-input`; never probes or product-source edits.
- **Technical review** may frame PE options, but an ADR cannot become Accepted
  while it invents user-visible behavior (T12).
- Outcomes map to pinned edges only (`pass` / `findings` / `needs-input` /
  `blocked` / `stale` / `failed`). See `references/handoff-envelope.md`.

## Explicitly deferred (not in this pin)

- Feasibility evidence probes
- Blocking security-gate / T13
- Task-level concurrency metadata (`parallel_safe` / `shared_files`)
- Automated wave merge or branch-cleanup Forge actions

## What we ask of the world

1. **Remount the pin** — no laptop `workflow.yaml` overlays.
2. **Read dispatch from the pin** — no skill-id allowlists in runners.
3. **Treat handoff + baton as durable state** — not chat.
4. **Partner changes** (launchpad materialize, Gateflow Enter-at) follow pin
   tags — see [for-launchpad.md](for-launchpad.md) and
   [for-gateflow.md](for-gateflow.md).

## Prompt packages and “eval”

Every packaged skill ships `prompts/` (versioned brief).  
`eval_before_promote` means: golden fixtures + consistency green before retag —
see [`../references/prompt-package-contract.md`](../references/prompt-package-contract.md).
That is **contract eval**, not a full agent behavioral harness.
