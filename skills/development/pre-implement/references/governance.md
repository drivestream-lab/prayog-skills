<!-- SYNC-COPY: byte-identical across pre-implement, initiative-feasibility, and
     spec-implementation-plan (skills/development/*/references/governance.md). Each dev
     skill must stay standalone-installable (npx skills add --skill <name>), so this
     content cannot be extracted to a shared folder outside the skill directory. If you
     edit this file, apply the identical edit to the other two copies in the same commit. -->

# Architecture governance (MDC + ADR)

Resolve paths from `.harness/profile.yaml` when present; else [layout-defaults.md](layout-defaults.md).

| Key | Typical path | Role |
|-----|--------------|------|
| `rules_glob` | `.cursor/rules/*.mdc` | How to implement — coding patterns and layer constraints |
| `adr_dir` | `docs/specification/adr` | What we decided — architectural constraints |

**MDC** = tactical implementation patterns (layer boundaries, auth helpers, logging, error handling, data validation).
**ADR** = strategic decisions (API shape, data ownership, auth model, cross-service contracts, infra boundaries).

ADRs may later be codified into MDC rules. Both must be checked — a spec can
violate an ADR before it violates a style rule.

---

## ADR pass — keyword-match then deep-read (before T2 Analyze)

Do not read all ADRs upfront. Use this filter:

1. List `{adr_dir}` — collect ADR titles + status (one line each).
2. Extract **domain keywords** from the spec or wave slice (e.g. data flow areas,
   module names, boundary names, integration types).
3. Match spec keywords to ADR titles. Include ADRs linked from `AGENTS.md` or
   tagged cross-cutting.
4. Read only **Accepted** ADRs whose title or tags match. Skip Superseded unless
   the spec explicitly cites one.
5. SKIPPED if `{adr_dir}` absent — state reason.

**Output of ADR pass:** a short table — ADR id | domain matched | status —
carried into the analysis phase as the constraint set.

---

## MDC pass — domain-filtered (before T2 Analyze / before coding)

Do not read all MDC files upfront. Filter by domain:

1. List all files under `{rules_glob}` by filename only — do not read yet.
2. From the spec or wave slice, identify which **engineering domains** are in scope
   (e.g. data layer, service boundary, CLI entrypoint, auth, messaging,
   observability, error handling, testing strategy, import layering).
3. Read only files whose names semantically cover the in-scope domains.
   Use filename keywords to judge relevance — you do not need to read a file to
   know its domain from its name.
4. Skip files whose domain is not touched by this spec or slice. Note skipped
   files with reason.
5. **Derive examples of what to flag from the content of the matched files.**
   Do not use examples from other repos or stacks — every repo's rules are different.

**Output of MDC pass:** a short table — MDC file | domain covered | read / skipped —
carried into the analysis phase.

---

## F13 / P12 — ADR conformance

For each spec wave or TASK touching architecture (data flow, boundary ownership,
cross-service contracts, deployment, storage model, CLI shape):

- Cite applicable ADR id, or `NEW-ADR` if the initiative introduces a decision
  not covered by any existing Accepted ADR.
- Flag spec wording that **contradicts** an Accepted ADR → finding (feasibility)
  or RISK row (plan). Severity: **Critical** if blocking.
- Flag **NEW-ADR** when spec chooses between alternatives with no existing ADR →
  PE question (feasibility; route to `/spec-technical-review`) or
  DEP/RISK + draft-ADR TASK (plan).

---

## F14 / P11 — MDC conformance

For each spec wave or TASK touching a domain covered by the filtered MDC set:

- Flag spec wording that implies a pattern **contradicting** a rule in
  `rules_glob`.
- Record in feasibility findings or plan TASK **MDC notes** column.
- If the discrepancy also touches architecture intent, cross-reference under
  ADR notes.

**Examples are repo-specific.** Derive them from the actual content of the
matched MDC files in this repo. Do not invent examples from other stacks.
