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

## Container images (CI)

Both forges run the same pipeline: `pytest` in an `ubuntu:24.04` job container,
then a kaniko build of the `runtime` stage. Neither runner exposes a Docker
daemon, which is why kaniko builds and why tests do not run inside the built
image.

| Workflow | Trigger | Result |
| --- | --- | --- |
| `.forgejo/workflows/ci.yml` | push to any branch | test, then build |
| `.forgejo/workflows/ci.yml` | push to `main` | test, build, push `git.turnerservices.cloud/thadigus/hamlib-rest:{latest,<sha>}` |
| `.github/workflows/ci.yml` | push to `main` (mirrored) | test, build, push `ghcr.io/thadigus/hamlib-rest:{latest,<sha>}` |

Forgejo jobs use `runs-on: docker`; GitHub jobs use `runs-on: self-hosted`.

Required secrets:

- Forgejo `PACKAGE_TOKEN` - a token with `write:package`, used for the Forgejo
  container registry.
- Forgejo `RENOVATE_TOKEN` - a token with repo and PR write access, used by
  `.forgejo/workflows/renovate.yml`.
- Forgejo `GITHUB_COM_TOKEN` - optional, a read-only github.com token that
  keeps Renovate off the anonymous API rate limit.
- GitHub needs none; the workflow pushes to GHCR with the built-in
  `GITHUB_TOKEN` and `packages: write`.

## Dependency updates

`renovate.json` drives Renovate. Alongside the stock managers it carries a
custom manager for the Hamlib release pinned in `flake.nix`, tracked against
GitHub releases of `hamlib/hamlib`. Renovate cannot compute a Nix hash, so
`.forgejo/update-hamlib-hash.sh` runs as a post-upgrade task and rewrites the
`sha256` to match the new tarball. That script is allow-listed through
`RENOVATE_ALLOWED_COMMANDS` in the workflow; renaming it means updating both.

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
