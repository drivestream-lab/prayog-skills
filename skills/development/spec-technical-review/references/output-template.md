# Technical Design Document — {INITIATIVE}

| Field | Value |
|-------|-------|
| Initiative | {INITIATIVE} |
| Spec | {SPEC_PATH} |
| Feasibility report | {FEASIBILITY_PATH} |
| Repo | {REPO} |
| Date | {YYYY-MM-DD} |
| Branch | `chore/INIT-{COMPONENT}-{NUMBER}-spec-{repo}` (spec PR — TDD committed here) |
| Initiative segment | `INIT-{COMPONENT}-{NUMBER}` — COMPONENT is service branch_code from service-catalog.yaml |
| Status | Draft |
| Review deadline | {YYYY-MM-DD + 5 business days} |
| Deciders | PE: {name} — explicit LGTM required, not approval by silence |

---

## 1. Problem statement

{1–3 sentences from spec. What engineering problem must be solved.}

---

## 2. Module / package boundaries

{List each module/package affected. For each: current state, proposed change,
ownership.}

| Module | Current state | Change | Owns |
|--------|---------------|--------|------|
| `{module}` | exists / stub / new | create / extend / unchanged | {layer} |

**Boundary diagram (text):**

```
{caller} → [{module A}] → [{module B}] → [{storage}]
             ↑ contract       ↑ contract
```

---

## 3. Public interface contracts

For each boundary crossing in section 2, specify the contract in
engineering terms (stack-agnostic — describe shapes and invariants, not syntax).

### 3.{n} `{ModuleA}` → `{ModuleB}`

**Method / entry point:** `{name}`
**Arguments:**
- `{arg}`: {shape description} — {invariant}

**Return:**
- `{field}`: {shape description}
- Error: {what is raised / returned on failure}

**Invariants:**
- {e.g. "output must validate against SchemaType schema"}
- {e.g. "no fabricated values — absent row preserved as null"}

---

## 4. ADR resolutions

One subsection per `NEW-ADR` finding from the feasibility report.

### 4.{n} Draft ADR — {short title}

**Feasibility finding:** {C-id or G-id}
**Status:** Draft — requires PE sign-off

**Problem:**
{1–2 sentences.}

**Options considered:**

| Option | Pros | Cons |
|--------|------|------|
| A. {option} | | |
| B. {option} | | |

**Recommendation:** Option {A/B} — {one-sentence rationale}

**Consequences:**
- {impact on other modules, test strategy, or future spec}

**Open for review by:** PE checkpoint

---

## 5. Test policy

| Module / area | Unit layer tests | Integration layer | Live verify | Golden test strategy |
|---------------|-----------------|-------------------|-------------|----------------------|
| `{module}` | {what is tested without I/O} | {what needs real deps} | {CLI/API smoke} | {exact / fuzzy / snapshot} |

**AI-output determinism policy (when applicable):**
- {e.g. "row count and schema validity: exact; extracted text fields: fuzzy
  match with configurable threshold; test approves snapshot manually on first run"}

---

## 6. Error handling strategy

| Failure mode | Module where it originates | Propagation path | Recovery |
|--------------|---------------------------|------------------|----------|
| {e.g. malformed xlsx} | extraction | raised to CLI boundary | terminal — exit non-zero, structured error message |
| {e.g. LLM timeout} | extraction | retry N times then raise | recoverable — configurable retry |

---

## 7. Observability contract

| Module | Log level | Structured fields | Notes |
|--------|-----------|-------------------|-------|
| `{module}` | INFO/WARNING/ERROR | {e.g. `file_path`, `schema_type`, `row_count`} | |

---

## 8. Data contract ownership

| Schema / data type | Owner (defines + validates) | Validation layer | Versioning |
|--------------------|----------------------------|------------------|------------|
| `{SchemaType}` | {module} | {edge / repository / both} | {immutable / semver / amend-by-PE} |

---

## 9. Resolved engineering decisions

All items from feasibility routed to PE lane. Every row must show a resolution.

| Finding ID | Question | Resolution | Default assumption if deferred |
|------------|----------|------------|-------------------------------|
| {C1/G1/…} | {engineering question} | {resolved: option chosen} / {deferred: reason} | {default} |

---

## 10. Routed out — product questions (PM)

These items remain open and require PM input before the implementation plan
is considered unblocked.

| # | Question | Blocks |
|---|----------|--------|
| PM-{n} | {product question — user-visible behaviour or scope} | {plan wave} |

---

## 11. Routed out — domain clarifications (SME)

| # | Question | SME / owner | Blocks |
|---|----------|-------------|--------|
| D-{n} | {business source-of-truth question} | {name / team} | {plan wave} |

---

## 12. Auto-fixed items

Items the agent resolved without human input (naming drift, inferred
cross-references, spec typos). These are **done** — no action required.

| ID | Item | Fix applied |
|----|------|-------------|
| AF-{n} | {e.g. CLI flag name drift} | {e.g. aligned spec to schema enum value} |

---

## 13. Implementation readiness verdict

| Gate | Status |
|------|--------|
| All T1–T10 checks | {PASS / FAIL — list blocking items} |
| Engineering decisions resolved | {N resolved, N deferred with defaults} |
| Draft ADRs written | {N drafts} |
| PM questions outstanding | {N — list} |
| Domain questions outstanding | {N — list} |
| **Ready for /spec-implementation-plan** | **YES / NO — reason** |

---

## Check summary

| Check | Status | Notes |
|-------|--------|-------|
| T1 Module boundaries | PASS/FAIL/SKIPPED | |
| T2 Interface contracts | | |
| T3 NEW-ADR resolutions | | |
| T4 Test policy | | |
| T5 Error handling | | |
| T6 Observability | | |
| T7 Data contract ownership | | |
| T8 Dependency graph | | |
| T9 Engineering questions zero | | |
| T10 PE sign-off gate | | |

---

## PR instructions

> Commit this TDD to the spec PR branch. PE reviews on the **same spec PR**.
> PE GitHub Approve = sign-off. Spec PR cannot merge until PE approves (when TDD present).
> CODEOWNERS enforces PE as a required reviewer on `Technical-Review-*`.

```
Branch:   chore/INIT-{COMPONENT}-{NUMBER}-spec-{repo}
PR title: "[INIT-{COMPONENT}-{NUMBER}] Spec — {repo}"
PR body:  link meta PRD PR; paste §13 Implementation readiness verdict when TDD is ready

Required reviewers (enforced by CODEOWNERS when TDD file is present):
  @{pe-name-or-pe-team}  ← must give explicit Approve, not just silence

Review deadline: {date from report header}
PE review checklist (PE works through this on the spec PR):
  [ ] T1 Module boundaries — can I draw the box?
  [ ] T2 Interface contracts — are shapes and invariants specified?
  [ ] T3 Draft ADRs — do recommendations make sense given existing ADRs?
  [ ] T4 Test policy — is determinism policy acceptable?
  [ ] T9 Zero unresolved PE items?

PE action:
  Approve → GitHub "Approve" on spec PR
  Request changes → spec PR thread with specific T-check item to fix

After PE approves:
  Dev updates §Status in this file: "Accepted — @{pe-name}  {date}"
  → /spec-implementation-plan can now run on the same branch
  → after plan is committed: merge spec PR, then seed board from plan §9
```
