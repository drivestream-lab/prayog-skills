# Ground spec — checks (G1–G10)

Run every check. PASS = zero open grounding findings that block sign-off.
SKIPPED = missing optional input (state reason). Fail closed when a required
check cannot run.

Ids: `../../../references/id-conventions.md`. Findings use **`GF-*`**, never
feasibility-owned `FF-*`.

| ID | Check | Evidence required |
|----|-------|-------------------|
| G1 | **Wave scope** | Grounding covers only the completed wave `W{N}` and REQs assigned to that wave by the plan / WorkManifest TASK `implements` lists — not every future REQ in the full product spec |
| G2 | **Ground command / evidence** | `{ground_command}` output included when defined; otherwise manual `source_roots` + `tests/**` scan documented. Unit (`{test_command}`) and live (`Live-Verify-*` / human evidence) are cited separately |
| G3 | **Assigned-REQ coverage** | Every wave-assigned `REQ-*` appears in the REQ checklist with verifiable artifact (entry point, test, live script, module boundary) |
| G4 | **Acceptance evidence** | Each assigned REQ maps to observable acceptance evidence from loop/live artifacts (`Wave-Execution-*`, `Live-Verify-*`, unit results) — not assertion-by-assertion duplication |
| G5 | **ADR boundaries** | Domain-filtered Accepted ADRs checked; no contradiction without an open `GF-*` |
| G6 | **MDC boundaries** | Domain-filtered `rules_glob` checked; pattern contradictions recorded as `GF-*` |
| G7 | **Contracts consumed / produced** | Consumed contracts match prior Ground Reports; §Contracts produced complete for next-wave `/pre-implement` |
| G8 | **Learning citations** | When `Learning-Extract-{INIT}-W{N}.md` exists, cite `L-*` ids only — do not re-author learning SSOT |
| G9 | **Stable GF-* findings** | Discrepancies use stable `GF-{nn}` ids; cite `REQ-*` in the row; blockers use `GF-*` not bare check numbers |
| G10 | **Complete handoff** | Canonical Ground Report path written; as-built row updated locally when appropriate; exact-head human sign-off package prepared; envelope stage `ground-spec` with outcome + next `wave-done-action` on pass (then `wave-signoff`) — no commit/merge by this skill |

Severity: **Blocking** (cannot `pass` to wave-signoff), **Should fix**, **Verify**.

**Blocking** when: G1 scopes future waves; G3 misses an assigned REQ; G7
§Contracts produced incomplete; G9 uses `FF-*` or unstable ids; G10 omits
handoff or claims merge/commit by this skill.
