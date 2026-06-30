## Pre-implement — {REPO} / {SLICE}

### Must read
- [ ] AGENTS.md
- [ ] rules_glob (MDC)
- [ ] Relevant ADRs: (list ADR ids read for this slice)
- [ ] (other concrete paths — spec slice, canon docs, plan wave)

### Governance alignment
- [ ] Slice spec aligns with listed ADRs (no silent contradiction)
- [ ] Plan TASK **MDC notes** / **ADR notes** for this wave reviewed
- [ ] `NEW-ADR` from plan has draft-ADR task complete or scheduled before encoding decision in code

### Must update (with code in same PR)
- [ ] product spec — path + section (tracker Spec path / initiative slice)
- [ ] as-built/implementation-status.md — verification row(s)
- [ ] as-built harness section (only if layout, CI, or overlap policy changes)
- [ ] tests_readme — feature map row (if coverage changes)
- [ ] unit_tests_dir — scope (edges, mocked dependencies)
- [ ] live_verify_dir — one live happy path per feature
- [ ] ADR — draft or update when plan flags `NEW-ADR` or decision changed

### Must not
- [ ] Edit `.cursor/rules/` submodule
- [ ] Duplicate unit assertions in live-verify
- [ ] Implement against spec wording that conflicts with Accepted ADR without superseding ADR first

### Test plan
| Layer | Proves | Command (from tests_readme) |
|-------|--------|------------------------------|
| unit | logic, branches, edges | (profile toolchain) |
| live-verify | product on running stack | per tests_readme |

### Tracker / PR
- Initiative: …
- Issue: #
- Spec path: docs/specification/product/…
- Verify command: (from board or plan)
- ADRs: (ids)

### Merge order (if cross-service)
(document dependency order or N/A)
