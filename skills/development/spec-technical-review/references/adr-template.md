# ADR-{NNN} — {title}

| Field | Value |
|-------|-------|
| Status | Draft |
| Initiative | {INITIATIVE} |
| Feasibility finding | {FINDING_ID} (`FF-*`) |
| Technical review | `{TDD_PATH}` |
| Source spec | `{SPEC_PATH}` |
| Source spec digest | `sha256:{hex}` |
| product_constraints | `[REQ-…, …]` — approved REQs this decision binds |
| changes_user_visible_behavior | `false` / `true` |
| spec_amendment_required | `false` / `true` |
| supersedes | `{ADR-… or none}` |
| superseded_by | `{ADR-… or none}` |
| Decision owner | PE |
| Approval evidence | Pending |
| Approved head | Pending |

> If `changes_user_visible_behavior` or `spec_amendment_required` would be
> `true`, **stop**: amend and re-approve the product spec before this ADR may
> become Accepted. Do not invent scope, UX, acceptance, priority, or business
> rules here.

## Product decisions excluded

List product choices this ADR deliberately does **not** make (owned by
approved `REQ-*` / PM):

- {e.g. “Whether one upload yields four outputs — see REQ-07”}

## Context

{Problem and constraints. Cite approved REQs and existing Accepted ADRs that
bound the design space. Do not introduce new user-visible behavior.}

## Options considered

| Option | Benefits | Costs / risks |
|--------|----------|---------------|
| A | | |
| B | | |

## Recommendation

{Selected option and rationale. Must satisfy `product_constraints` without
amending product behavior.}

## Consequences

- {Positive and negative consequences.}

## Revisit triggers

- {Observable condition that would justify superseding this ADR.}

## Lifecycle — Accepted immutability and supersession

Once `Status: Accepted`, do **not** rewrite the accepted body in place.
To change the decision:

1. create a new ADR that `supersedes` this one,
2. set this ADR's `superseded_by` to the new id and status `Superseded`,
3. record owner, date, and review evidence on both files.

## Acceptance finalization

After PE review comments are resolved and PE explicitly states the decision is
ready for acceptance — **and** product-boundary fields remain `false` —
update the file before final GitHub approval:

```text
Status: Accepted
Decision owner: @{pe-name}
Approval evidence: {review/comment URL}
Approved head: {full SHA to be approved}
product_constraints: [REQ-…]
changes_user_visible_behavior: false
spec_amendment_required: false
```

The formal PE GitHub Approve must be on the final commit containing this
Accepted metadata. No file changes occur after that approval (publish via
Forge `/commit-workspace` — not inside content skills).
