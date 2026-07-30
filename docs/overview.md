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
  pre-implement → loop-spec → live-verify     # human prove + patch tip
       → wave-awaiting-closeout               # park (not wave-complete)

PASS 2 (Enter-at learning-extract, or human /learning-extract)
  learning-extract → ground-spec → wave-signoff
```

- `verify` is **manual** (optional aid) — not on the Pass-1 edge.
- **Co-ship live verify:** when a wave adds/changes a product surface, the same
  wave ships the live script under `live_verify_dir` (plan P15). `/loop-spec`
  runs check+unit only; the human executes the script at `live-verify` before
  Pass-2 closeout automation continues.
- Checkpoints use **purpose-named ids** (`prd-impact-acceptance`,
  `coding-readiness`, `live-verify`, `wave-signoff`). GitHub labels stay
  lane-named (`impact-map-*`, `spec-*`).

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
