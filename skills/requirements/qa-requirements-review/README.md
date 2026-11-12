# /qa-requirements-review

```text
/qa-requirements-review
```

Pass one PRD path. Default is the promoted `prd/{INIT}.md`. A named
candidate is allowed and is labeled `prd_status: candidate`.

Writes (overwrite):

- `{reports_dir}/QA-Requirements-Review-{INIT}.md`

Asks testability questions (`QQ-*`) for gaps (`QG-*`) on checks R1–R12.
`ready_for_test_design: yes` means every blocking question is answered.

Re-run with answers to record them and to ask follow-ups. Answered ids stay.

Does not write test cases, edit the PRD, or call `/qa-test-design`.
