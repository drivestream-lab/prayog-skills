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
  pre-implement → wave-pr-action → loop-spec → live-verify
       → wave-awaiting-closeout               # park (not wave-complete)

PASS 2 (Enter-at learning-extract, or human /learning-extract)
  learning-extract → ground-spec → wave-signoff
```

- `pre-implement` is **gate-only** (read-only board/head checks). It never opens
  a wave branch or implements product code — that belongs to Forge + `loop-spec`.
  It consumes the canonical §9 WorkManifest (`prayog/v1`) and fails closed when
  the shared contract check fails, a TASK lacks exit proof, or an applicable
  wave lacks a live-verification contract/script.
- On `pre-implement.pass`, next is **`wave-pr-action`** (reuse `open_draft_pr`
  with `title` / `body_path` / `head_ref` / `base_ref`). There is **no** merge
  Forge action — merge stays human-only at `wave-signoff`.
- `loop-spec` executes WorkManifest tasks in dependency order within declared
  file scope; records observed proof in `Wave-Execution-*` / handoff without
  mutating approved manifest intent; runs check+unit only; creates planned live
  scripts but never claims human smoke/sandbox success. Emits one stage-level
  `commit_workspace` readiness package after the wave is green (no per-TASK
  commits inside the content skill).
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
- **WorkManifest authority (Initiative B):** Prayog owns `prayog/v1`. Board tickets
  and stage artifacts project or record evidence — they are not a second
  execution-intent authority. Validator: `scripts/workmanifest_contract.py`;
  plan check P16; predicate `workmanifest-contract-pass`.
- Checkpoints use **purpose-named ids** (`prd-impact-acceptance`,
  `coding-readiness`, `live-verify`, `wave-signoff`). GitHub labels stay
  lane-named (`impact-map-*`, `spec-*`).

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
