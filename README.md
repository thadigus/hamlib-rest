# Hamlib REST API Server

A FastAPI-based authenticated REST wrapper for Hamlib rig control.

Hamlib REST API is a Python-based REST API for Hamlib, written with FastAPI. This project makes the Hamlib library more accessible for frontend web frameworks such as React. It also serves as a server for multiple client frontends to connect and operate amateur radio transceivers.

This project provides a fully authenticated **REST API** for controlling amateur radio equipment via **Hamlib**, with complete support for:

* Frequency control
* Mode/width control
* VFO selection
* Split operation
* Levels (RF power, mic gain, etc.)
* RIT/XIT
* PTT
* Repeater offset/shift
* Power state
* Configuration parameters

All rig commands are exposed as **REST endpoints**, and the server includes **session-based authentication**, **USB device discovery**, and **auto-generated OpenAPI documentation**.

## Docs

This repo includes a static docs site in `docs/` with:

* Project overview (`docs/index.md`)
* Getting started guide (`docs/getting-started.md`)
* Operations/command coverage (`docs/operations.md`)
* OpenAPI reference (`docs/openapi.md`)
* Deployment guide (`docs/DEPLOYMENT.md`)
* Architecture notes (`docs/ARCHITECTURE.md`)
* Command reference (`docs/API_COMMANDS.md`)

For deployment, use the included GitHub Pages workflow:

* `.github/workflows/pages.yml`
* `mkdocs.yml`

The docs site is generated with MkDocs using the ReadTheDocs theme.

See:

* `docs/README.md`
* `docs/API_COMMANDS.md`

## Features

### Full Hamlib Capability Exposure

Every major rig control function is wrapped:

* get/set frequency
* get/set mode & filter width
* get/set VFO
* get/set split (mode, TX freq, TX VFO)
* get/set RIT and XIT
* get/set PTT
* get/set power
* get/set repeater settings
* get/set levels
* Hamlib configuration parameters

### Session-based Rig Instances

Each authenticated user session maintains its own rig object.
Multiple rigs / users can operate in parallel.

### Auto-Generated Swagger UI

Navigate to: http://localhost:8080/docs

To explore and interact with all rig commands.

### Unit Tests + Container CI

The repo includes pytest-based unit tests. CI runs on a self-hosted Forgejo
instance; the GitHub mirror publishes images for public consumption.

* `.forgejo/workflows/ci.yml` - every branch push runs `pytest`, then builds
  the `runtime` image with kaniko. Pushes to `main` also publish
  `git.turnerservices.cloud/thadigus/hamlib-rest` as `:latest` and `:<sha>`.
* `.github/workflows/ci.yml` - pushes to `main` run the same test and build,
  publishing `ghcr.io/thadigus/hamlib-rest`.
* `.github/workflows/pages.yml` - publishes `docs/` to GitHub Pages.
* `.forgejo/workflows/renovate.yml` with `renovate.json` - opens dependency
  PRs, including the Hamlib release pinned in `flake.nix`.

Run tests locally:

```bash
pytest
```

## Project Structure

```
.
├── main.py                    # FastAPI application with all endpoints
├── lib/
│   ├── auth.py                # Session authentication
│   ├── hamlib_driver.py       # Pythonic wrapper around Hamlib.Rig
│   ├── hamlib_constants.py    # Hamlib enum/model introspection helpers
│   └── rig_manager.py         # Rig lifecycle management
├── schemas.py                 # Pydantic models for request/response bodies
├── docs/                      # Static docs site
├── Dockerfile                 # Docker file to build the project and run in a container
└── README.md                  # This file
```

## Installation

### Docker Implementation (Recommended)

This project has been built from the ground up to run on Docker. You can simply build the container and run it, passing through whatever devices you would like, or handing it `--privileged`.

```bash
docker build -t hamlib-rest ./
docker run --privileged -p 8080:8080 hamlib-rest
```

Swagger UI at http://localhost:8080/docs

## License

MIT
