# ID map (orientation)

Procedure and field SSOTs:

| Doc | Role |
|-----|------|
| [`../references/id-conventions.md`](../references/id-conventions.md) | Product / process / delivery ids |
| [`../references/artifact-write-contract.md`](../references/artifact-write-contract.md) | Canonical paths; no `*-revN` siblings |
| [`../references/handoff-envelope.md`](../references/handoff-envelope.md) | Persistent handoff; blockers use stable ids |

## Quick map (current pin)

```text
PRD CAP-* / REQ-* / OQ-*
  → validate VF-*
  → review CHG-* (linked to VF-*)
  → update PRD
  → impact map (Impact-Map-{INIT}.md, map_revision++)
  → prd-impact-acceptance (checkpoint) → merge
  → spec REQ-* (legacy FR-* ≡ same number)
  → plan TASK-* implements REQ-*
  → coding-readiness (checkpoint) → spec merge
  → /create-board-tickets — EPIC → W* (TASK table in wave body)
  → Pass-1: pre-implement → loop-spec (TASK-*) → live-verify
  → Pass-2: learning-extract (L-*) → ground-spec (REQ checklist + cite L-*)
  → wave-signoff
```

## Defaults

- Product id: **`REQ-*`** canonical  
- Board: TASK ids in **wave issue body**  
- Learning: **`L-*`** in Learning-Extract artifact (DB SSOT is Gateflow)  
- PM/dev reports: **overwrite** canonical paths only  
