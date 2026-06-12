## Pre-implement — {REPO} / {SLICE}

### Must read
- [ ] (concrete paths)

### Must update (with code in same PR)
- [ ] product spec — path + section (tracker Spec path / initiative slice)
- [ ] as-built/implementation-status.md — verification row(s)
- [ ] as-built harness section (only if layout, CI, or overlap policy changes)
- [ ] tests/README.md — feature map row (if coverage changes)
- [ ] tests/unit/ — scope (edges, mocked repos)
- [ ] tests/verify/ — one live happy path per feature
- [ ] ADR — only if decision changed

### Must not
- [ ] Edit `.cursor/rules/` submodule
- [ ] Duplicate unit assertions in verify

### Test plan
| Layer | Proves | Command (from tests/README.md) |
|-------|--------|--------------------------------|
| pytest | logic, branches, edges | make test |
| verify | product on running API | per tests/README.md |

### Tracker / PR
- Initiative: …
- Issue: #
- Spec path: docs/specification/product/…
- Verify command: (from board or plan)

### Merge order (if cross-service)
(document dependency order or N/A)
