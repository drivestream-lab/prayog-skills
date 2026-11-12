---
name: qa-requirements-review
description: >-
  Reviews one PRD as a QA expert. Inventories stated requirements and
  acceptance criteria, finds testability gaps, and asks clarifying
  questions and follow-ups. Use when the user asks for a QA review of a
  PRD, a quality layer on requirements, requirement gaps, clarifying
  questions, or preparation for test design. Writes
  {reports_dir}/QA-Requirements-Review-{INIT}.md. Does not write test
  cases, edit the PRD, score the delivery bar, or invent product
  behavior. Human-invoked; not a workflow node.
disable-model-invocation: true
---

# QA requirements review

Read **one** PRD as a QA expert. Record what it states. Find places a test
would have to guess. Ask those questions. On a later run, ask a follow-up
only when an answer opens a new decision.

The test pack is `/qa-test-design`. Delivery-bar scoring is `/prd-quality`.
Semantic audit is `/validate-requirements`. Leave those jobs in those skills.

**Pin contracts (read, do not fork):**

- Ids: `prayog-skills/references/id-conventions.md` (`QG-*`, `QQ-*`)
- Paths: `prayog-skills/references/artifact-write-contract.md`
- Rubric and shape: [references/gap-rubric.md](references/gap-rubric.md),
  [references/review-template.md](references/review-template.md)

## Inputs

1. **One PRD path.** Default `prd/{INIT}.md` (`prd_root` from
   `.harness/profile.yaml`). A named candidate is allowed. Review that file
   only. Two paths → ask which file. Do not blend.
2. **Initiative id** — from the filename, the PRD, or ask.
3. **Prior review** (optional) — `{reports_dir}/QA-Requirements-Review-{INIT}.md`
   when this is a re-run. `{reports_dir}` from `.harness/profile.yaml`
   (meta default `prd/reports/`).
4. **Answers** (optional) — the user message, else the prior file's Answers
   cells. Quote the answer used. If the message and the file disagree, use
   the message and say so.

## Output

Overwrite `{reports_dir}/QA-Requirements-Review-{INIT}.md`.
Bump `review_revision` by 1 (start at 1). Never write `*-revN`.
Never edit the PRD.

## NON-NEGOTIABLE

1. **Quote, then judge.** Inventory rows carry a PRD quote. A gap cites the
   quote a test cannot turn into an expected result.
2. **Closed rubric.** Checks are R1–R12 in
   [references/gap-rubric.md](references/gap-rubric.md). Do not add a check
   mid-run.
3. **One gap, one question, when an answer is required.** Mint `QG-{nn}` and
   `QQ-{nn}` together. Notes that need no answer get no id.
4. **Blocking** means a test would have to guess the actor, the expected
   result, the layer (`ui` / `be` / `both`), or a numeric or time bound.
5. **Ids survive re-runs.** Answered `QQ-*` stay. New follow-ups take the
   next free id. Set `follows` to the parent `QQ-*`.
6. **Ask in the chat reply.** The file is the record. The reply asks the
   open questions in `QQ` order.
7. **Stop while any blocking `QQ` is open.** `ready_for_test_design` is
   `yes` only when that set is empty. Do not draft cases in the reply.
8. **Do not invoke** `/qa-test-design`, `/prd-think`, `/prd-quality`,
   `/validate-requirements`, `/review-findings`, `/update-documents`,
   `/prd-impact-map`, or forge. Do not mint `OQ-*`, `IM-*`, `PQ-*`, `Q-*`,
   `CAP-*`, `J-*`, or `REQ-*`.

## Process

### T0 Resolve

Name the PRD path, whether it is `promoted` or `candidate`, the initiative
id, `review_revision`, and the output path. Read the PRD and, on a re-run,
the prior review.

### T1 Inventory

List every `REQ-*`, stated acceptance criterion, `CAP-*`, `J-*`, actor, and
stated negative or error outcome. Quote. Do not add meaning by paraphrasing.
A requirement with no acceptance criterion stays on the inventory and is
reviewed under R1.

### T2 Gaps

Apply R1–R12 to the inventory. For each hit that needs a decision, mint the
next `QG-{nn}` and `QQ-{nn}`. Record check id, REQ ids, quote, blocking
`yes` or `no`, and the decision the answer must make.

### T3 Answers and follow-ups

When answers are present, mark those `QQ-*` `answered` and store the quote.
Re-read only the REQs that answer touches. Mint a follow-up when the answer:

- names a condition, actor, limit, or exception the PRD does not already
  state, and a test would still have to guess which one applies, or
- is still subjective, or still defers the decision ("sometimes", "it
  depends", "as appropriate").

Leave answered ids in place. Do not re-ask them.

### T4 Write

Write the report from
[references/review-template.md](references/review-template.md).

`ready_for_test_design` is `yes` only when every blocking `QQ` is
`answered`. Unanswered non-blocking questions stay `open` and do not flip
the flag.

### T5 Ask

Reply in this order:

1. `ready_for_test_design` and the output path.
2. Each **open** question, blocking first: id, the REQ it blocks, the
   decision needed, and the question itself. For a follow-up, cite the
   parent answer in one line.
3. When the flag is `yes`, name `/qa-test-design` as the next command.
   When it is `no`, ask for answers and a re-run of this skill.

## Workflow handoff

This skill is **human-invoked**. It is not a node in pinned `workflow.yaml`.

When orchestrator-bound:

1. Persist `{reports_dir}/QA-Requirements-Review-{INIT}.md`.
2. **Overwrite** `handoff_path` with the `handoff:` envelope when bound.
   Leaving the baton empty is a failed stage for automated consumers.
3. Derive `next_candidates` and `human_checkpoint` from pinned root
   `workflow.yaml` for `(stage: qa-requirements-review, outcome)` per
   `prayog-skills/references/handoff-envelope.md` (**Derive from pinned
   workflow**). Set `human_checkpoint: true` only when the resolved next
   node's `type` is `human-checkpoint`.
4. This `skill_id` is absent from `workflow.yaml`, so the derivation has
   no edge: `next_candidates: []`, `human_checkpoint: false`,
   `external_action: false`. Put the recommended command only in
   `signals.recommended_next` (`qa-test-design` or `answer-questions`).
5. `outcome` is `needs-input` when any blocking `QQ` is open, else `pass`.
6. `blockers` lists those open blocking `QQ-*` ids. Empty on `pass`.

When not orchestrated, skip baton write unless `handoff_path` is bound.
