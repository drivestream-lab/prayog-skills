# Gap rubric (R1–R12)

Closed set for `/qa-requirements-review`. Cite the check on the gap
(`QG-04`, check `R3`). The check number is not a handoff blocker.

A hit that needs a human decision mints one `QG-{nn}` and one `QQ-{nn}`.
A hit that is already decided by a quote is not a gap. An observation that
needs no decision is a **Note** with no id.

## Blocking

`blocking: yes` when a later test would have to guess any of:

- the actor
- the expected result (what is true when the test passes)
- the layer: `ui`, `be`, or `both`
- a numeric or time bound the words already imply ("fast", "large", "recent")

Otherwise `blocking: no`. Unanswered non-blocking questions do not stop
`/qa-test-design`. Design must not invent the missing detail.

## Checks

| Id | Gap | Ask when |
|----|-----|----------|
| R1 | REQ has no acceptance criterion | A pass/fail observation is missing |
| R2 | Quantifier, threshold, or timing is unnamed | Words imply a bound and no number or limit is stated |
| R3 | Pass condition is subjective | "Fast", "intuitive", "appropriate", "user-friendly", and the same class of words |
| R4 | Negative or error outcome is missing | The REQ implies rejection, failure, or denial and no observable failure is stated |
| R5 | Actor or permission is unnamed | More than one actor exists, or an action is restricted, and the text does not say who |
| R6 | Layer is unnamed | The outcome could be judged on a screen, a service, or both, and the PRD does not say which |
| R7 | Input, bound, or empty state is missing | The REQ names a field, search, upload, or collection and not the empty or limit case it depends on |
| R8 | Lifecycle or state transition is incomplete | Start state, end state, or the trigger is missing |
| R9 | External dependency failure is unnamed | The REQ depends on a vendor, queue, or other service and timeout or failure behavior is absent |
| R10 | Contradiction | Two quotes in the same PRD cannot both be true |
| R11 | Stated criterion is not observable | The criterion cannot be checked by a person or a probe |
| R12 | Stated criterion traces to no REQ | An acceptance criterion sits outside every `REQ-*` |

Use the closest check. Do not mint R13.

## Question shape

- One question asks for one decision.
- Name the REQ ids it unblocks.
- When the PRD already implies a closed set, offer those options and an
  explicit "none of these" so a new answer can appear.
- When the gap is a product decision, say so in the question. The answer
  is stored here. Updating `prd/{INIT}.md` stays on the PM chain
  (`/validate-requirements` → review → update). This skill does not write
  the PRD.
- Follow-up: set `follows` to the parent `QQ-*`, quote the answer that
  opened the new decision, and ask only the new decision.

## Ids

`QG-01`, `QQ-01` — exactly two digits. Keep ids across `review_revision`s.
Do not recycle an id. Do not mint `OQ-*`, `IM-*`, `PQ-*`, or `Q-*`.
