# update-documents

Propagates approved changes across related documents without making new
semantic decisions.

- **Resolution mode:** consumes `Resolution-*.md`, presents its change set for
  visibility, then requires approval of the exact change manifest.
- **Ad-hoc mode:** requires approval of both the user-provided change set and
  the exact change manifest.

New ownership, scope, product, engineering, or open-question decisions route
back to `review-findings`; they are not invented during propagation.

**Original author:** rushikeshpol02 (ai-skills). **Maintainer:** drivestream-lab.

## Invoke

```
/update-documents
```

Typical input: `prd/reports/Resolution-INIT-PRAYOG-001.md` from `review-findings`.

Scope: PRD + `cross-service-lab.md` + per-repo `03-integrations.md`. Re-run `validate-requirements` (incremental) after PRD edits.

See repo root README for install command.
