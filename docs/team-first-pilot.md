# Team-first SDD workflow pilot

## Objective

Exercise the pinned Prayog workflow with mandatory human gates before any
automation or review policy is relaxed.

## Required scenarios

| Scenario | Expected behavior |
|----------|-------------------|
| Clean single-repo handoff | Approved map opens exactly one spec scope |
| Legacy initiative PR | PR readiness blocks until reconcile/supersede decision |
| Cross-repository contract | Provider/consumer contract is complete before feasibility |
| Repository added or removed | Ripple action opens, holds, or closes the correct work |
| Material PRD change | Gate 1 becomes stale and affected scopes re-enter review |
| Dependency order change | Existing implementation plan routes to re-plan |
| Board seed | Runs only after spec merge and creates one issue per wave |
| Wave execution | Verify precedes ground; human approval follows ground evidence |

## Pilot targets

- Zero stale or out-of-scope gate escapes.
- D1–D12 pass before feasibility.
- Zero critical requirement leakage after spec approval.
- Zero contract churn caused by omitted required fields.
- Every GitHub external action has explicit authorization.
- Every workflow stage persists a `sdd-delivery/v2` handoff.

## Review policy

Every generated spec receives engineering review. Every required TDD receives
PE review. Every Ground Report receives a human checkpoint. Approval by silence
is not permitted.

## Graduation

Do not move to sampled or exception-only review until at least five
representative initiatives complete with zero gate escapes and the engineering
team accepts the measured thresholds.
