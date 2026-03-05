# Deployment Notes

## Docs (GitHub Pages)

Docs are published by:

- `.github/workflows/pages.yml`
- `mkdocs.yml`

The workflow builds markdown from `docs/` using MkDocs (`readthedocs` theme), then publishes the generated static site to GitHub Pages.

Enable Pages in repository settings:

1. Open **Settings** -> **Pages**
2. Set **Build and deployment** to **GitHub Actions**
3. Push to `main` or run the workflow manually

## Backend (Hamlib + FastAPI)

Deploy backend separately in an environment with Hamlib and hardware access.

Example:

```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

## Security recommendations

- Replace default credentials in `lib/auth.py`
- Put API behind HTTPS reverse proxy
- Restrict API exposure to trusted network/VPN
- Audit and monitor rig control access
