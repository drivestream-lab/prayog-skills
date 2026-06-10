# v1 granularity — Epic + one task per repo

## Default for INIT initiatives

Unless the user explicitly requests **fine** granularity, produce:

```
EPIC (prayog-meta)
├── C1  prayog-compose   — seed + stack for initiative
├── P1  prayog-parichay  — first app merge
├── A1  prayog-abhilekh  — depends_on: [P1]
└── O1  prayog-ops       — depends_on: [A1]
```

**Total:** 1 epic + 4 tasks for a four-repo delivery map (INIT-PRAYOG-001 pattern).

## Why one task per repo

- Matches Chapter 8 sprint flow: one `feature/INIT-*` branch per repo per initiative phase.
- Keeps Project board readable before sub-splitting.
- `seed-work` + Project hierarchy still gives epic → task tree.
- Finer breakdown (login vs assets vs BFF routes) belongs in **implementation PRs** or a future `fine` mode — not v1 manifest.

## When to use fine granularity

Only when the user says e.g. "split parichay into login + session tasks" or "bootstrap-style multi-issue manifest".

Fine mode rules:

- Keep epic as parent for all items.
- Preserve merge-order `depends_on` across repos.
- Within a repo, order items by dependency (spec before code, API before verify).
- Do not exceed **8 tasks** without explicit PM approval (board noise).

## INIT-PRAYOG-001 task content guide

| id | Repo | Slice summary | Key PRD refs |
|----|------|---------------|--------------|
| C1 | prayog-compose | FrostMart seed SQL, JWT secret env, Redis, reading fields | §10, AC-001, §5 |
| P1 | prayog-parichay | `POST /api/v1/auth/login`, JWT claims, Redis session | §4, FR-001, AC-002 |
| A1 | prayog-abhilekh | Asset create/list, store scope, reading fields | §5, §6, FR-002–005 |
| O1 | prayog-ops | BFF login + assets, `prayog_sid`, portal UI | §4 browser, §6, FR-001–004 |

## Merge order vs depends_on

| Concept | Source | Manifest |
|---------|--------|----------|
| Git merge order | PRD Appendix A | `depends_on` between repo tasks |
| Compose startup | Runtime | **Not** encoded as hard dep (compose ∥ parichay) |
| Verify order | §11 | Listed in bodies; optional note in epic |

## Excluded from v1 work list

- prayog-meta documentation tasks (playbook edits) — covered by epic or separate chore PRs
- prayog-meta `cross-service-lab.md` updates — handoff Phase 2 already merged
- Per-repo `as-built` updates — checklist inside each task body, not separate issues
