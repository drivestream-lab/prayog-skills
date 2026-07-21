---
name: ui-lock-finalize
description: >-
  After PM selects a UI variation, delete ALL temporary explore variants
  (including the selected one), restore the pre-explore frontend baseline, and
  write LOCKED-{INIT}.md as the only durable UI contract for planning and
  /loop-spec. Runs on the Draft spec PR before /spec-implementation-plan.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, docs/project-guidance/**, components/**, app/**
---

# UI lock finalize (cleanup + lock artifact)

Runs **after** `ui-variation-lock` (human) when the initiative has UI.
Produces the durable lock contract and a **clean** tree for later waves.

## NON-NEGOTIABLE

1. Resolve paths from `.harness/profile.yaml` when present.
2. Prerequisites:
   - `/ui-variations` completed on this spec PR
   - Variation brief has **Selected** + **Improvements** filled
3. **Delete all explore scaffolding** — variants A, B, **and C/selected**,
   temporary preview switches (`?variant=` or equivalent), and any explore-only
   wiring. Restore the **pre-explore** frontend baseline. Do **not** leave the
   selected composition in the tree.
4. The production UI for the locked choice is **not** built here — `/loop-spec`
   builds it later from `LOCKED-{INIT}.md` + the implementation plan on a
   clean baseline.
5. Write durable lock artifact (default path below). Commit on the Draft spec PR.
6. Do not start `/spec-implementation-plan` until cleanup is done and the lock
   file is saved.
7. No design-tool MCP / codegen JSX paste.

## Chain position

```
/ui-variations → ui-variation-lock (human) → /ui-lock-finalize ← YOU ARE HERE
    ↓ pass
/spec-implementation-plan → … → /pre-implement → /loop-spec
  (loop-spec builds the locked composition on the clean tree)
```

## Workflow

```
- [ ] 1. Read Selected + Improvements from the variation brief
- [ ] 2. Remove ALL explore variant files and preview switches
- [ ] 3. Confirm tree matches pre-explore baseline for touched paths
- [ ] 4. Write LOCKED-{INIT}.md (build contract only — no explore code)
- [ ] 5. Lint/build to confirm cleanup did not break the baseline
- [ ] 6. Hand off to /spec-implementation-plan
```

### Lock artifact

Default path:

`docs/project-guidance/design-system/variations/LOCKED-{INIT}.md`

```markdown
# Locked UI variation — {INIT}

| Field | Value |
|-------|-------|
| Selected | A / B / C |
| Pattern / shell | `<pattern-id>` |
| Route / surfaces | `/…` |
| Approver | @… — date |
| Source brief | `docs/project-guidance/design-system/variations/INIT-{id}.md` |

## Composition contract (must follow in waves)

{Describe the selected option’s layout, hierarchy, density, and primary actions
so /loop-spec can rebuild it on a clean tree.}

## PM improvements (must follow)

- …

## Cleanup attestation

- [x] All temporary explore variants removed (including selected)
- [x] Preview switch removed
- [x] Frontend baseline restored for explore-touched paths
```

## Verify

Consumer lint + build from `AGENTS.md` / profile must pass on the cleaned tree.

## Forbidden

- Leaving any A/B/C explore files or preview switches
- Keeping the selected variant as production code in this step
- Planning or `/loop-spec` before this stage completes on UI initiatives
- Changing product scope beyond documenting the lock

## Workflow handoff

Append the envelope from `../../../references/handoff-envelope.md`.
Use stage `ui-lock-finalize`.

- `pass` → `spec-implementation-plan`
- `needs-input` / `blocked` → human decision
- `stale` → `ui-variations`
- `failed` → stop

Record in `signals`:

- `ui_locked: true`
- `selected: A|B|C`
- `lock_path: docs/project-guidance/design-system/variations/LOCKED-{INIT}.md`
- `explore_cleaned: true`
