# Architecture governance (MDC + ADR)

Resolve paths from `.harness/profile.yaml` when present; else skill `references/layout-defaults.md`.

| Key | Typical path | Role |
|-----|--------------|------|
| `rules_glob` | `.cursor/rules/*.mdc` | How to implement — coding patterns |
| `adr_dir` | `docs/specification/adr` | What we decided — architectural constraints |

**MDC** = tactical patterns (i18n keys, semantic tokens, auth helpers, logging, forms).  
**ADR** = strategic decisions (API verbs, data ownership, auth model, cross-service contracts, infra boundaries).

ADRs may later be codified into MDC rules. Both must be checked — spec can violate an ADR before it violates a style rule.

## Relevant ADR pass (before deep read)

1. List `{adr_dir}` (index or `ADR-*.md` titles + status).
2. Match initiative spec keywords and waves (API, BFF, auth, cache, polling, i18n, deployment, module, …).
3. Include ADRs linked from `AGENTS.md` or tagged cross-cutting.
4. Read **Accepted** ADRs in scope; note **Superseded** only if spec cites them.
5. SKIPPED if `{adr_dir}` absent — state reason.

## MDC pass

Read all files matching `rules_glob` before T2 Analyze in feasibility and plan.

## F13 / P12 — ADR conformance

For each spec wave or TASK touching architecture (API shape, auth, data flow, cross-service, deployment, IaC):

- Cite applicable ADR id, or `NEW-ADR` if the initiative introduces an undocumented decision.
- Flag spec wording that **contradicts** an Accepted ADR → finding (feasibility) or RISK row (plan). **Critical** if blocking.
- Flag **NEW-ADR** when spec chooses between alternatives not covered by existing ADRs → PM question (feasibility) or DEP/RISK + draft-ADR TASK (plan).

## F14 / P11 — MDC conformance

For each spec wave or TASK touching UI, BFF, API handlers, or forms:

- Flag spec wording that implies literal user-facing strings, raw color utilities, wrong auth client, wrong BFF handler pattern, manual polling instead of cache invalidation, or other conflicts with `rules_glob`.
- Record callouts in feasibility findings or plan TASK **MDC notes** column.
- Discrepancies that affect architecture intent may also belong under ADR notes if an ADR governs the area.

Stack-specific examples (apply only when matching rules exist in the repo):

- i18n keys not literal UI strings
- semantic tokens (`text-destructive`, `text-warning`) not raw Tailwind colors
- `authFetch` for authenticated client calls
- `createApiLogger` / `proxyAbhilekhPlatformJson` for BFF route handlers
- TanStack Query `invalidateQueries` not manual polling
