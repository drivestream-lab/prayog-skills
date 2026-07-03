---
name: ground-spec
description: >-
  Validate a completed wave implementation against its product spec FRs, repo
  artifacts, and cross-spec contracts. Produces a Ground Report including a
  Contracts Produced section that is the required input for pre-implement of
  the next wave. Use when a wave claims complete, before human checkpoint, or
  when asked to ground a spec.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, src/**
background_eligible: true
background_trigger: "all wave tasks complete (loop-spec exits green)"
---

# Ground spec

Validate implementation against the **product spec** and **actual repo
artifacts** — not PRD text alone. Produce a Ground Report that the **next
wave's `/pre-implement` consumes as a contract baseline**.

## NON-NEGOTIABLE

1. Run the repo's automated ground check when `{ground_command}` is defined
   in the harness profile. Include full output in the report. If `{ground_command}`
   is not defined, perform manual FR validation by reading `source_roots` directly.
2. Check every **FR** in the product spec — map each to a verifiable artifact
   (test result, entry point, module boundary, verify script output).
   Use engineering terms: "entry point", "module boundary", "output shape" —
   not language-specific terms.
3. Check cross-spec contracts: modules from this wave may only consume
   interfaces from prior waves as documented in those waves' Ground Reports.
4. Check boundary rules per ADRs and domain-filtered MDC rules.
5. **Do not** mark spec `human_approved` — that is a human gate only.
6. **Populate the Contracts Produced section** — this is the structured
   handoff that enables `/pre-implement` for the next wave. Without it,
   the chain is broken.

## Chain position

```
/loop-spec (all iterations green)
    ↓
/ground-spec                          ← YOU ARE HERE
  produces: Ground-Report-W{N}.md
            └── §Contracts produced   ← pre-implement for WN+1 reads this
    ↓
  human checkpoint
  → as-built W{N} = human_approved
    ↓
/pre-implement (next wave)
  reads: Ground-Report-W{N}.md §Contracts produced
```

## Read order

1. `AGENTS.md`
2. Product spec: `docs/specification/product/` — relevant spec for this wave
3. `docs/specification/as-built/implementation-status.md`
4. Ground reports of prior waves (for cross-spec contract baseline)
5. Relevant ADRs
6. Ground check output (`{ground_command}`) + unit verification result (`{test_command}`)

## Output format

Save report to `{reports_dir}/Ground-Report-{SPEC}-W{N}.md` (from profile or layout-defaults).

```markdown
# Ground report — {SPEC} W{N}

| Field | Value |
|-------|-------|
| Wave | W{N} — {wave title} |
| Spec | {SPEC_PATH} |
| Date | {YYYY-MM-DD} |
| Branch | `feature/{sc}-w{N}-{slug}` — same branch as wave code |
| Status | Draft |
| Review deadline | {YYYY-MM-DD + 2 business days} |
| Deciders | Tech lead / reviewer: {name} — explicit LGTM required |

## Automated check output
(paste full output of {ground_command} / {verify_command})

## FR checklist
| FR | Spec claim | Verified artifact | Status |
|----|-----------|-------------------|--------|
| FR-N.N | {claim} | {entry point / test / verify script} | pass / fail / partial |

## Boundary checks
(Derived from domain-filtered ADRs and MDC rules for this repo.)
| Rule | Source | Status |
|------|--------|--------|

## Cross-spec contracts consumed
(What this wave assumed from prior waves — confirm each still matches.)
| Assumed contract | Source | Match? |
|-----------------|--------|--------|
| {entry point / schema / command} | Ground-Report-W{N-1} | yes / NO — drift |

## Discrepancies (must fix before human checkpoint)
| ID | FR | Finding | Severity |
|----|----|---------|---------|

## Contracts produced by this wave
(REQUIRED — this section is the input for /pre-implement of the next wave.
Describe in engineering terms: module, entry point name, input shape,
output shape, invariants. Do NOT use language-specific syntax.)

| Contract | Module / component | Entry point | Input shape | Output shape | Invariants | Next wave |
|----------|--------------------|-------------|-------------|--------------|------------|-----------|
| {name} | {module} | {callable/command/endpoint} | {accepts} | {returns/emits} | {guarantees} | W{N+1} |

## PR instructions

> Commit this report + updated as-built row to the wave branch (last commit
> before PR is marked ready). Ground report and code are reviewed together
> on the same PR — do not open a separate PR for the ground report.

Branch:   feature/{sc}-w{N}-{slug}  ← same branch as wave code
PR title: "[{sc} W{N}] {slug} — implementation + ground report"
PR body:  paste FR checklist summary + §Contracts produced table

Required reviewer: per CODEOWNERS in this repo
Review deadline: {date from header}

After reviewer approves:
  Update as-built: W{N} → human_approved
  Merge PR
  → /pre-implement for W{N+1} gate check will pass

## Ready for human checkpoint?
yes / no — reason

Human must:
- [ ] Review FR checklist — all pass or explicitly deferred
- [ ] Review §Contracts produced — accurate and complete for next wave
- [ ] Mark as-built: {SPEC} W{N} = human_approved
```
