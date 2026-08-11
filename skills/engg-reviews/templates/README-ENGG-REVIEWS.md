# engg-reviews PE workspace (installed from pe-rc-2)

Gate-independent PE pack. Does **not** unlock Gate 1 or `/spec-draft`.

## Skills linked under `.agents/skills/`

- `ensure-repo-graph`
- `prd-codebase-map`
- `review-product-questions` (optional PE stance refine)
- `post-product-questions`

## Layout

```text
pe-workspace/          ← open Cursor here
  .agents/skills/      → symlinks into prayog-skills cache @ pe-rc-2
  bin/refresh-graph.sh
  fleet.yaml
  graphs/<repo>/
  out/reports/
```

Sibling clones: `../{meta}` and `../{app-repos}` at `develop`.

## Quick start

```bash
# edit fleet.yaml
./bin/refresh-graph.sh <repo>              # code-only + graph.html
# ./bin/refresh-graph.sh <repo> --with-docs  # needs .env OPENAI_API_KEY

# In Cursor:
/ensure-repo-graph
/prd-codebase-map
/review-product-questions    # optional
/post-product-questions      # Meta PR comment after authorize
```

Re-install / upgrade:

```bash
python3 /path/to/install_engg_reviews.py --target . --ref pe-rc-2 --force
```
