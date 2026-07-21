---
name: ui-variations
description: >-
  On the Draft spec PR, before the implementation plan, produce three temporary
  runnable UI composition options for PM lock. Non-UI initiatives skip. After
  human lock, do not finalize here — /ui-lock-finalize cleans all explore code
  and writes LOCKED-{INIT}.md. Product-agnostic; prefer the frontend profile.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, docs/project-guidance/**, components/**, app/**
---

# UI variations (explore before plan)

Runs on the **Draft spec PR** after feasibility (and technical-review approval
when applicable), **before** `/spec-implementation-plan`.

Explore only: three temporary compositions for human selection. Production UI
for the locked choice is built later in `/loop-spec` on a clean tree.

## NON-NEGOTIABLE

1. Resolve paths from `.harness/profile.yaml` when present.
2. Run only while the Draft spec PR is open (`chore/*-spec-*` or equivalent).
3. If the initiative has **no UI** (API/infra/docs-only): emit handoff `skipped`
   with reason → `/spec-implementation-plan`. Do not invent UI work.
4. Produce **three** temporary runnable options that share the **same** UI
   pattern id / shell contract; vary **composition/layout/density** only.
5. Compose existing `components/ui` and established domain components — no new
   shared primitives unless consumer change-control allows it later in waves.
6. Do **not** treat explore code as the production deliverable. After PM lock,
   `/ui-lock-finalize` **deletes all** explore variants (including the selected
   one) and restores the pre-explore baseline.
7. Do **not** paste design-tool MCP / codegen JSX verbatim.
8. Stop after requesting human review — do not run `/ui-lock-finalize` or
   `/spec-implementation-plan` in this stage.

## Chain position

```
/initiative-feasibility (pass) or technical-review-approval
    ↓
/ui-variations          ← YOU ARE HERE (explore)
    ↓ pass
ui-variation-lock (human) → /ui-lock-finalize → /spec-implementation-plan
    ↓ skipped (non-UI)
/spec-implementation-plan
```

## Workflow

```
- [ ] 1. Confirm UI-in-scope from initiative spec
- [ ] 2. Resolve pattern/shell from consumer pattern catalog or project-guidance
- [ ] 3. Note pre-explore baseline (paths touched) for later full cleanup
- [ ] 4. Scaffold three temporary compositions (variant A/B/C)
- [ ] 5. Wire a temporary preview switch (?variant= or equivalent)
- [ ] 6. Write variation brief markdown (options + empty human-lock fields)
- [ ] 7. Request human review — stop
```

### Scope fields

| Field | Use |
|-------|-----|
| Route / surface | Where variations render |
| Pattern / shell id | **Same** for all three options |
| UX job | What every variation must still accomplish |
| Primary actions | Must remain reachable in every variation |
| Visual non-goals | Hard limits for all three |

### Three variations

| Rule | Detail |
|------|--------|
| Same pattern | Do not invent three patterns — vary composition only |
| Meaningful diff | Layout, density, or information hierarchy — not trivial spacing |
| Primitives | Existing UI kit + domain components |
| i18n | Dev-only labels OK; production copy in `/loop-spec` |
| BFF / API | Reuse existing contracts — do not add new domain APIs here |

Suggested layout (adapt to consumer conventions):

```text
components/{domain}/<view>-variant-a.tsx
components/{domain}/<view>-variant-b.tsx
components/{domain}/<view>-variant-c.tsx
components/{domain}/<view>.tsx   ← temporary switch on ?variant=
```

### Variation brief

Create or update under consumer guidance (default):

`docs/project-guidance/design-system/variations/INIT-<id>.md`

```markdown
# Variation brief — INIT-<id>

| Field | Value |
|-------|-------|
| Route / surfaces | `/…` |
| Pattern | `<pattern-id>` |
| Spec PR | |

## Variations

| Id | Summary | Preview |
|----|---------|---------|
| A | … | local preview URL |
| B | … | … |
| C | … | … |

## Human lock (fill after review)

- **Selected:** A / B / C
- **Improvements:** …
- **Approver:** @… — date
```

### Human gate

Post on the Draft spec PR (or board, per consumer convention) asking for
selection + improvements. **Do not** proceed to finalize or plan until
**Selected** and **Improvements** are filled.

## Verify (explore only)

Run the consumer’s lint + build commands from `AGENTS.md` / profile so previews
work. Full token lint + unit tests for production UI belong in `/loop-spec`.

## Forbidden

- Leaving explore variants as the long-term implementation
- Finalizing route map / as-built / pattern catalog in this step
- Three different pattern ids for one surface
- Design-tool JSX paste
- Running `/spec-implementation-plan` before `/ui-lock-finalize` on UI inits
- Skipping cleanup (that is `/ui-lock-finalize`)

## Workflow handoff

Append the envelope from `../../../references/handoff-envelope.md`.
Use stage `ui-variations`.

- `pass` → `ui-variation-lock` (human)
- `skipped` → `spec-implementation-plan` (non-UI initiative)
- `needs-input` / `blocked` → human decision
- `stale` → `initiative-feasibility`
- `failed` → stop

Record variation brief path and explore file paths under `signals`.
