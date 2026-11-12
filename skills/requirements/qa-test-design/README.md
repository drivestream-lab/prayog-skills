# /qa-test-design

```text
/qa-test-design
```

Requires `{reports_dir}/QA-Requirements-Review-{INIT}.md` with
`ready_for_test_design: yes`, or an explicit accepted-risk list of the
open blocking `QQ-*` ids.

Writes (overwrite, one `pack_revision`):

- `{reports_dir}/QA-Test-Plan-{INIT}.md`
- `{reports_dir}/QA-Test-Cases-{INIT}.md`
- `{reports_dir}/QA-Acceptance-Criteria-{INIT}.md`
- `{reports_dir}/QA-RTM-{INIT}.md`

The plan's **Automation handoff** is the brief for the agent that designs
UI automation, backend automation, or both. This skill writes no
automation code and does not edit the PRD.

Start at the plan. Cases with `automation_ready: yes` are in scope for
that agent. Accepted-risk rows have no case.
