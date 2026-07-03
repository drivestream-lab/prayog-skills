## Pre-implement — {REPO} / {WAVE} — {SLICE TITLE}

---

### Gate check (prior wave)

> Complete this before reading anything else. Do not proceed if the gate fails.

| Item | Required | Status |
|------|----------|--------|
| Prior wave as-built row | `human_approved` | [ ] {wave id} = {status} |
| Prior Ground Report exists | `reports/Ground-Report-{SPEC}-W{N-1}.md` | [ ] exists / missing |
| Plan PE sign-off (W0 only) | Implementation-Plan §0 marked complete | [ ] complete / pending |

**Gate verdict:** PASS / BLOCKED — {reason if blocked}

---

### Contracts consumed (from prior Ground Report)

> Read `Ground-Report-{SPEC}-W{N-1}.md §Contracts produced`.
> For each contract this slice depends on, confirm the actual built interface
> matches what this wave's spec assumes.
> Scan `source_roots` to confirm — do not rely on spec text alone.

| Assumed contract | Entry point | Input shape | Output shape | Source | Confirmed? |
|-----------------|-------------|-------------|--------------|--------|------------|
| {what this wave assumes} | {module/component — entry point name} | {accepts} | {returns/emits} | Ground-Report-W{N-1} | [ ] yes / NO — drift detail |

**Unconfirmed contracts** (prior wave not yet grounded or source not found):
- {list any contracts this wave needs that have no Ground Report backing}
  → Flag as risk before opening branch.

---

### Must read

- [ ] `AGENTS.md`
- [ ] MDC rules (domain-filtered — list files read for this slice's domains):
  - [ ] {rule file} — {domain it covers}
- [ ] ADRs (keyword-matched — list ids):
  - [ ] ADR-{N} — {what it governs for this slice}
- [ ] Spec: {path to product spec for this wave}
- [ ] Plan wave section: `reports/Implementation-Plan-{initiative}.md` W{N}

---

### Governance alignment

- [ ] Slice spec does not contradict any listed ADR
- [ ] Plan TASK MDC notes and ADR notes for this wave reviewed
- [ ] Any NEW-ADR from the plan has a draft-ADR task scheduled before the
  decision is encoded in code

---

### Must update (in the same change as the code)

- [ ] Product spec — {path + section}
- [ ] `as-built/implementation-status.md` — verification row for this wave
- [ ] `tests_readme` — feature map row if verification coverage changes
- [ ] Unit verification scope — edges and boundary behaviour (mocked dependencies)
- [ ] Live verification — one end-to-end happy path per feature
- [ ] ADR — draft or update when plan flags NEW-ADR or a decision changed

---

### Must not

- [ ] Implement against spec wording that contradicts an Accepted ADR without
  first superseding that ADR
- [ ] Duplicate unit verification assertions in live-verify scripts
- [ ] Assume a contract from a prior wave is correct without checking the
  Ground Report (or flagging it as unconfirmed above)

---

### Verification plan

| Layer | What it proves | Command (from tests_readme / profile) |
|-------|----------------|---------------------------------------|
| Unit | Module logic, boundary behaviour, edge cases (no external I/O) | {from profile} |
| Live verify | Product behaviour on running stack | {from tests_readme} |
| Ground check | All FRs satisfied; boundaries respected | {from profile} |

---

### Tracker / PR

- Initiative: {initiative id}
- Issue: #{board issue — from seed-work output}
- Spec path: {docs/specification/product/…}
- Verify command: {from board issue or plan}
- ADRs in scope: {ids}

---

### Merge order (if cross-module / cross-service)

{document dependency order or N/A}
