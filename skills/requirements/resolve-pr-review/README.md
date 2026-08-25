# resolve-pr-review

End-to-end Gate 1 **PE/tech-lead comment resolution** for meta PRD / impact-map PRs.

**Problem solved:** Review feedback often triggers multiple re-review rounds because
agents fix only the numbered items in the comment while leaving stale cross-references,
rubber-stamped validation, digest mismatches, abbreviated map sections, and live PR
body drift. This skill closes **all** objections in one pass by treating the PRD as
SSOT, regenerating the impact map from scratch, syncing every satellite file, and
running a commit gate before posting a reply.

**Does not replace** `review-findings` (validation-report workshop) or
`update-documents` (Resolution propagation). Use when a **reviewer comment on an open
Gate 1 PR** requests changes.

## Invoke

```
/resolve-pr-review 121 latest
```

Or paste the reviewer comment text with PR number / initiative id.

Inputs: meta PR number (or URL), reviewer comment (or `latest`), optional product
decisions already made by PM.

Outputs: PRD + outline + validation report + impact map (new revision) + PR body;
draft reply comment. **Never posts** until user approves.

See `prayog-skills/references/artifact-write-contract.md` and
`prayog-skills/references/handoff-envelope.md`. Repo root README for install.
