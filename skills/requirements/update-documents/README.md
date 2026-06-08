# update-documents

Propagates approved changes across related documents with two mandatory approval gates (change set + change manifest).

**Original author:** rushikeshpol02 (ai-skills). **Maintainer:** drivestream-lab.

## Invoke

```
/update-documents
```

Typical input: `prd/reports/Resolution-INIT-PRAYOG-001.md` from `review-findings`.

Scope: PRD + `cross-service-lab.md` + per-repo `03-integrations.md`. Re-run `validate-requirements` (incremental) after PRD edits.

See repo root README for install command.
