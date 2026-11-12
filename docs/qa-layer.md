# QA layer — PRD to automation input

**Purpose:** operator flow for a QA pass on one PRD. Normative procedure
lives in each skill's `SKILL.md`. This page only orients humans.

The pack is the brief for a later agent that designs test automation
(UI, backend, or both). These skills write no automation code.

## Role separation

| Skill | Job | Writes |
|-------|-----|--------|
| `/qa-requirements-review` | Inventory, gaps, questions, follow-ups | `{reports_dir}/QA-Requirements-Review-{INIT}.md` |
| `/qa-test-design` | Plan, cases, enhanced acceptance criteria, RTM | `QA-Test-Plan-{INIT}.md`, `QA-Test-Cases-{INIT}.md`, `QA-Acceptance-Criteria-{INIT}.md`, `QA-RTM-{INIT}.md` |

Review **asks**. Design **specifies tests**. `/prd-quality` **scores**.
`/validate-requirements` **audits**. Do not collapse these jobs.

## Operator chain

```text
one PRD (promoted or a named candidate)
  → /qa-requirements-review
  → answer blocking QQ-*  (re-run the review; follow-ups only if needed)
  → /qa-test-design
  → automation-design agent reads the plan's Automation handoff
```

**Rules:**

- One PRD per run. A candidate is labeled `prd_status: candidate`.
- `ready_for_test_design: yes` means every blocking question is answered.
- Design refuses while a blocking `QQ-*` is open, unless the user names
  those ids as accepted risk. Accepted risk writes no case.
- The pack does not edit `prd/{INIT}.md`. A product decision still goes
  through validate → review → update when it should live in the PRD.
- Both skills are in `profiles/meta-pm.yaml` `requirements_skills` and are
  **not** workflow nodes. Entrypoint of the PM walk stays
  `/validate-requirements`.

## What the automation agent receives

Start at `QA-Test-Plan-{INIT}.md`, section **Automation handoff**
(`prayog-qa-pack/v1`).

| `layer` | Automation |
|---------|------------|
| `ui` | UI |
| `be` | Backend |
| `both` | Both, observations kept on the layer the case names |

| `rung` | Environment |
|--------|-------------|
| `unit` | Process and mocks |
| `capability` | Real infra, one ability |
| `journey` | Real infra, multi-step |

Cases with `automation_ready: yes` are in scope. The agent preserves
`REQ-*`, `EAC-*`, `TC-*`, `CAP-*`, and `J-*`.

## Ids

| Id | Meaning |
|----|---------|
| `QG-*` | Testability gap |
| `QQ-*` | Clarifying question |
| `EAC-*` | Enhanced acceptance criterion |
| `TC-*` | Test case |

`QQ-*` is not `OQ-*`, `IM-*`, `PQ-*`, or `Q-*`.
