# Persistent handoff envelope

Every Prayog stage ends with a handoff block in its durable output artifact.
Chat summaries may repeat it, but chat is not workflow state.

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: initiative-feasibility
  outcome: findings
  artifact:
    path: docs/specification/reports/Initiative-Feasibility-Report-INIT-001.md
    digest: sha256:{hex}
  blockers:
    - F-12
  signals:
    new_adr: true
  next_candidates:
    - spec-technical-review
  human_checkpoint: false
  external_action: false
```

## Required fields

| Field | Meaning |
|-------|---------|
| `contract` | Delivery contract implemented by the producer |
| `stage` | Node id from `workflow.yaml` |
| `outcome` | One of the contract outcomes |
| `artifact.path` | Durable stage output |
| `artifact.digest` | Digest of the output after it is saved |
| `blockers` | Stable finding/question ids that prevent progress |
| `signals` | Stage-specific routing facts; never implicit prose |
| `next_candidates` | Workflow-valid next nodes, not an authorization to execute |
| `human_checkpoint` | Whether a human decision is required next |
| `external_action` | Whether the next transition can mutate GitHub or another system |

## Navigation rules

1. Read the latest handoff and the pinned `workflow.yaml`.
2. Verify the handoff contract matches the installed contract.
3. Resolve the transition for the recorded outcome.
4. Explain the next action before executing it.
5. Never auto-transition a human checkpoint.
6. Never perform an external action without explicit authorization.
7. A stale artifact routes to the workflow's stale transition, not the nominal
   next skill.

## Outcome vocabulary

- `pass` — stage criteria are satisfied.
- `findings` — durable findings require a workflow-defined resolution path.
- `needs-input` — required information is unavailable.
- `blocked` — an explicit gate prevents progress.
- `stale` — an upstream artifact or approval no longer matches.
- `failed` — execution or verification failed.
- `skipped` — stage is legitimately inapplicable with a recorded reason.

Stage-specific statuses such as `PR READY`, `approved`, or `partial` belong
under `signals`; they map to one of the standard outcomes.
