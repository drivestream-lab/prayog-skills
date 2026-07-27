# IDs and artifact write contract

Human overview of conventions shipped on `features/rc-2`. Skills are the
procedure SSOT; this page is orientation only.

| Doc | Role |
|-----|------|
| [`references/id-conventions.md`](../references/id-conventions.md) | Product / process / delivery ids |
| [`references/artifact-write-contract.md`](../references/artifact-write-contract.md) | Canonical paths; no `*-revN` siblings |
| [`references/handoff-envelope.md`](../references/handoff-envelope.md) | Persistent handoff; blockers use stable ids |
| [`references/prompt-package-contract.md`](../references/prompt-package-contract.md) | Versioned skill invocation briefs (`prompts/`) |

## Quick map

```text
PRD CAP-* / REQ-* / OQ-*
  → validate VF-*
  → review CHG-* (linked to VF-*)
  → update PRD
  → impact map (same Impact-Map-{INIT}.md, map_revision++)
  → spec REQ-* (legacy FR-* ≡ same number)
  → plan TASK-* implements REQ-*
  → board EPIC → W* (TASK table in wave body)
  → loop-spec binds TASK-* ; failures → blockers
  → ground REQ-* checklist
```

## Defaults used in this change set

- Product id: **`REQ-*`** canonical
- Board: TASK ids in **wave issue body** (sub-issues per TASK optional)
- PM reports: **overwrite** canonical paths only
