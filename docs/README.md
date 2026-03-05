# Docs Directory

This directory is markdown-only source content for the documentation site.

## Files

- `index.md`
- `getting-started.md`
- `operations.md`
- `openapi.md`
- `API_COMMANDS.md`
- `ARCHITECTURE.md`
- `DEPLOYMENT.md`

## Site generation

GitHub Pages builds the docs using MkDocs with the ReadTheDocs theme.

- Configuration file: `mkdocs.yml`
- Workflow: `.github/workflows/pages.yml`

## Local preview

```bash
pip install mkdocs
mkdocs serve
```

Default URL: `http://127.0.0.1:8000`
