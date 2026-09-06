# Hamlib REST API Server

### **This is not a client application.**

### A FastAPI-based authenticated REST wrapper for Hamlib rig control

Hamlib REST API is a Python based REST API for Hamlib, written with FastAPI, supporting both OpenAPI and Swagger. This project is written to make the Hamlib library more accessible for frontend web frameworks such as React. This also has a convient second function of becoming a server for multiple client front ends to connect and operate amatuer radio transcievers.

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

---

# Docs

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

---

# Features

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

Navigate to: <http://localhost:8080/docs>

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

---

# Project Structure

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

---

# Installation

### Docker Implementation (Recommended)

This project has been built from the ground up to run on Docker. You can simply build the container and run it, passing through whatever devices you would like, or handing it `--privileged`.

```bash
docker build -t hamlib-rest ./
docker run --privileged -p 8080:8080
```

Navigate to: <http://localhost:8080/docs>

### Development Container

For a repeatable local dev environment, the repo includes a `.devcontainer` setup that reuses the provided `Dockerfile`.

1. Install the **Dev Containers** (or **Remote Containers**) extension in VS Code.
2. From this folder run **“Dev Containers: Reopen in Container”** (or run `devcontainer up --workspace-folder .` from the CLI).
3. VS Code will build the container, mount the workspace at `/code`, and forward port `8080`.

Once inside the container you can use the built-in Python interpreter (`/usr/bin/python3`) and launch the API with `uvicorn main:app --reload --host 0.0.0.0 --port 8080`.

#### USB serial devices inside the devcontainer

Hamlib needs direct access to USB serial devices. Dev Containers let you pass host devices into the container using per-user overrides so you do not have to commit machine-specific paths:

1. Copy `.devcontainer/devcontainer.local.json.example` to `.devcontainer/devcontainer.local.json` (this file is gitignored).
2. Edit the `runArgs` array to list each device you want to expose using the normal Docker `--device=/dev/ttyUSBx` syntax.
3. (Optional) Keep the `mounts` entry or point it at any other `/dev/serial/by-id/...` path you want so the familiar udev symlinks are available inside the container.
4. Rebuild/Reopen the devcontainer.

The Docker Engine must also be able to reach the device (e.g. on Linux the user running Docker needs to be in the `dialout` group). Once the container restarts, the ports you listed in `devcontainer.local.json` appear inside `/dev` and Hamlib can use them normally.

---

# Authentication

This server uses simple session-based authentication.

1. Login to create a session:

```
POST /login
```

The server returns:

```json
{
  "session_id": "abcdef123456",
  "user": "..."
}
```

2. Use this `session_id` as a query parameter for all rig commands:

```
GET /rig/frequency?session_id=abcdef123456
```

Sessions also act as namespaces:
each session gets its own rig instance.

---

# Initialize the Rig

Before sending rig commands you must initialize it:

```
POST /rig/init?session_id=abcdef123456
```

Body:

```json
{
  "model": 229,
  "port": "/dev/ttyUSB0",
  "baud": 4800
}
```

Supports any Hamlib rig model number.

---

# Rig Commands Overview

Once initialized, you can:

### Frequency

```
GET  /rig/frequency
POST /rig/frequency
```

### Mode

```
GET  /rig/mode
POST /rig/mode
```

### VFO

```
GET  /rig/vfo
POST /rig/vfo
```

### Split

```
GET  /rig/split
POST /rig/split
```

### Levels

```
GET  /rig/level
POST /rig/level
```

### RIT / XIT

```
GET  /rig/rit
POST /rig/rit
```

```
GET  /rig/xit
POST /rig/xit
```

### PTT

```
GET  /rig/ptt
POST /rig/ptt
```

### Power

```
GET  /rig/power
POST /rig/power
```

### Repeater

```
GET  /rig/repeater
POST /rig/repeater
```

### Configuration Parameters

```
GET  /rig/config/params
POST /rig/config
```

---

# Example Use Case

This REST server is ideal for:

* Web-controlled ham radio dashboards
* Remote station control
* Python/Javascript rig automation
* Logging software
* Node-RED or Home Assistant integrations
* Integrating Hamlib with custom UIs or cloud services

---

# Contributing

Pull requests are welcome!
Please open an issue for:

* New rig commands
* Missing Hamlib features
* API design improvements

---

# License

MIT License — Free to use in any project.
