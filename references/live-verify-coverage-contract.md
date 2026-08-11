# Live-verify coverage contract (SSOT)

What a `live_verify_dir` artifact must self-declare so its `REQ-*` coverage
survives after the `PURGE` plan that co-shipped it is gone, and how planners
check for reuse before writing a new artifact.

See also: [artifact-write-contract.md](artifact-write-contract.md) (durable
identity), [workmanifest-contract.md](workmanifest-contract.md) (`verification.live`
shape), [id-conventions.md](id-conventions.md) (`REQ-*`).

## Why this exists

`verification.live.covers` in the WorkManifest is the only place a wave's live-verify
coverage is declared today, and the WorkManifest lives in `Implementation-Plan-{INIT}.md`
— `PURGE` at initiative closure. Once purged, nothing durable says what a given
script or runbook actually verifies. A later planner facing a similar surface has
no way to check for an existing candidate to extend, so the default becomes
"write a new file" every time — the coverage fact, not the file count, is the
missing durable thing.

## The marker

One line, anywhere in the artifact's first ~20 lines, containing the literal
substring:

```text
prayog:covers: REQ-01, REQ-02
```

**Deliberately not a code-comment-specific format.** The marker is a plain
text substring, discoverable by a literal search — not a per-language comment
syntax. It works identically:

- Inside a Python `#` comment or docstring.
- Inside a TypeScript/Go/Java `//` comment.
- Inside an HTML comment in a markdown runbook (`<!-- prayog:covers: REQ-01 -->`),
  or as a plain visible line (`**Covers:** REQ-01, REQ-02`) when the artifact is a
  human-run checklist rather than executable code — confirmed against a real
  markdown-runbook-shaped verify artifact, not a hypothetical.

The artifact itself is `KEEP` (`artifact-write-contract.md` — "product source /
unit tests / live-verify **scripts**"). The marker inherits that automatically;
no separate classification is needed.

## Resolution — via `files[]`, never by parsing `command`

Do **not** try to derive "the file to check" by parsing the `command` string.
`command` is a free-text invocation (`python tests/verify/verify_foo.py`,
`npm run verify:foo`, or a plain-English pointer to a runbook for a human to
follow) — it is not reliably a bare, parseable file path, and for some stacks
it may not name an executable file at all.

Resolve instead via the TASK's own **declared `files[]` entries** with
`action: create` or `action: modify` under the profile's `live_verify_dir` —
those are already explicit, repo-relative, unambiguous paths regardless of
stack or artifact shape.

## Overlap check (required before declaring a new FILE — P15)

Before a plan declares a new `live_verify_dir` FILE, state which existing
artifacts were checked for overlap with the new surface's `REQ-*`/capability
family (via `scripts/verify_coverage_query.py`, below) and, if none was
extended, why. See `spec-implementation-plan/references/checks.md` P15.

## Query tool

`scripts/verify_coverage_query.py` scans a `live_verify_dir` for the marker
and answers `--req REQ-01`, `--wave INIT-X:W3`, `--capability CAP-04`, or
`--dump` (full listing). **Read-only, stdout only** — it never writes a
tracked artifact. There is no "current listing" file to keep in sync; the
index is computed fresh on every call.

## Cross-check at plan time (workmanifest_contract.py)

`scripts/workmanifest_contract.py`'s `_validate_live` optionally resolves
each wave's `files[]` entries under the workspace root, reads any file
carrying the marker, and fails closed when the manifest's `verification.live.covers`
and the artifact's self-declared coverage are both present and disjoint. When
no candidate file carries a marker at all (legacy artifact, best-effort
backfill), this is not an error — coverage cannot yet be independently
checked, not that it is wrong. The check only runs when a workspace root is
supplied (`--base-path` / `validate_workmanifest(..., base_path=...)`); omit
it and the check is skipped, not failed.

## Optional codegrapher drift-check (later, not required to ship this)

When a codegraph provider is available (see
[codegraph-tool-contract.md](codegraph-tool-contract.md)), a skill **may**
additionally spot-check that the marker's cited module/REQ linkage still
looks structurally real, and record any mismatch under `signals`. This is a
drift-check layered on top of a contract that already works without it —
never a requirement, never a blocker.

## Non-goals

Not retrofitting all existing artifacts with markers in one pass —
best-effort backfill, new/extended artifacts comply going forward. Not
changing `P5`/`P16` or any check unrelated to live-verify coverage.
