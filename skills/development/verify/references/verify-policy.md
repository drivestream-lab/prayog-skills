# Verify policy (Python backend)

| Layer | Location | Proves |
|-------|----------|--------|
| Unit | `tests/unit/` | Logic, branches, edge cases (mocked repos) |
| Verify | `tests/verify/` | Product feature on **running** service |
| Debug | `tests/debug/` | Exploration — not gating |

**No overlap:** do not assert the same behavior in unit and verify for the same feature.

**Commands:** read `tests/README.md` for env activation, config files, bootstrap scripts, and exact verify invocations. Do not hardcode repo-specific env names in the skill — defer to the runbook.

**Constitution:** `.cursor/rules/testing-verify-flows.mdc`

**After verify:** update `implementation-status.md` live-verified column; paste command in PR and tracker Verify field.
