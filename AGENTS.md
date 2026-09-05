# Hamlib REST API Server - Agent Steering Guide

Expectations for AI coding agents working in this repository. This is a
radio-control REST service (a FastAPI wrapper around Hamlib rig control), not
infrastructure - adapt accordingly.

## Agent Purpose

1. **Carry out specific code prescriptions** - execute the changes asked for.
2. **Planning assistance via research** - search for Hamlib/rigctl
   documentation (hamlib docs, rigctl man page), protocol details (CI-V,
   serial), and prior art; return findings with sources.

Lean on the Hamlib documentation and the OpenAPI contract
(`openapi.yaml`) rather than internal knowledge alone; verify rig behavior
against a live or dummy rig where possible.

---

## Documentation Policy

- **`docs/`** is AI-authored project documentation (MkDocs site, ReadTheDocs
  theme) and is expected to exist and be maintained. This is the only location
  where AI should be writing documentation and commentary.
- **The code is documented well**: public classes and methods carry
  docstrings, and `README.md` plus `docs/` cover usage. That is the
  documentation deliverable.
- **Keep implementation internals comment-light.** Names and structure
  self-explain. A comment earns its line only where the code genuinely
  cannot state the intent (a Hamlib quirk, a non-obvious constant mapping).
  No narration, no restating the code.
- **`openapi.yaml` is generated, not hand-edited.** After any route,
  schema, or parameter change, regenerate it from the app (script in
  `docs/openapi.md` §Regenerate) and commit the result. It is copied into
  the published docs site by the Pages workflow.
- Prose (docs, READMEs, docstrings) follows the [Writing Style](#writing-style)
  rules below.

When reviewing existing docs, report technical inaccuracies, drift between
code and docs, and drift between code and `openapi.yaml`.

---

## Code Style

**Goal**: minimal, clean, self-explanatory code.

- **Python**: type hints on public APIs. Dependencies come from distro
  packages (`fastapi`, `uvicorn`, `Hamlib` bindings - see `Dockerfile`);
  add a runtime dependency only when a distro package cannot cover it.
  Prefer clarity over cleverness. Keep `lib/` modules focused on their layer:
  `hamlib_driver.py` wraps `Hamlib.Rig`, `rig_manager.py` owns per-session
  lifecycle, `auth.py` owns sessions.
- **Shell scripts** (e.g. `debug/`): POSIX (`#!/usr/bin/env sh`), `set -eu`,
  no bashisms, functions under 20 lines.
- No inline comments except where the code cannot express the constraint
  itself.

---

## Project Conventions

### Repository Layout

- Single top-level Python project (the REST server); no per-directory
  subprojects.
- `main.py` - FastAPI app with all endpoints.
- `lib/` - `auth.py` (session auth), `hamlib_driver.py` (rig wrapper),
  `hamlib_constants.py` (Hamlib constant/model introspection),
  `rig_manager.py` (per-session rig lifecycle and lock).
- `schemas.py` - Pydantic request/response models.
- `docs/` - MkDocs site; `openapi.yaml` - generated OpenAPI contract;
  `openapi.md` documents how to regenerate it.
- `tests/` - pytest tests, all runnable without hardware.
- `debug/` - helper scripts (source `debug/init_dummy_rig.sh` to get a
  `SESSION_ID` against a running server).
- `Dockerfile` - multi-stage: `runtime` (server) and `test` (pytest);
  `.devcontainer/` reuses it.

### Python tooling

- No venv, no pip, no uv in this repo. Dependencies are distro packages
  installed in the `Dockerfile` (Ubuntu 24.04: `python3-fastapi`,
  `python3-hamlib`, `uvicorn`, ...; tests add `python3-pytest`,
  `python3-httpx`).
- Run the server: `uvicorn main:app --host 0.0.0.0 --port 8080`
  (Swagger UI at `http://localhost:8080/docs`).
- Run tests: `pytest` (configured in `pytest.ini`). CI runs them inside
  the `test` image: `docker build --target test -t hamlib-rest:test . &&
  docker run --rm hamlib-rest:test`.
- Live experimentation: start the server, then source
  `debug/init_dummy_rig.sh` to open a dummy rig (model 1, `/dev/null`) and
  use `$SESSION_ID` with `curl`.

### Secrets

- **Never commit secrets.** `lib/auth.py` currently carries a hardcoded
  `VALID_USERS` store; any new credential must come from environment
  variables, never from code. `debug/` scripts prompt for credentials at
  runtime - keep it that way.
- Check `.gitignore` before committing; keep venvs, capture logs, and
  `.devcontainer/devcontainer.local.json` out of git.

---

## Review & Quality

Before proposing changes, verify:

1. **Imports**: the app imports without error
   (`python3 -c "import main"`).
2. **OpenAPI in sync**: if routes/schemas changed, `openapi.yaml` was
   regenerated (see `docs/openapi.md`).
3. **Tests pass**: `pytest` green - the API is exercised against a dummy
   rig, so nothing requires hardware.
4. **No secrets**: nothing sensitive tracked.

The dummy rig (model 1, port `/dev/null`) is the local stand-in for a real
radio: any live behavior check should run against it. Real rig runs happen
in the container with host devices passed through (`--device` or
`--privileged`); see `docs/DEPLOYMENT.md` and the devcontainer notes in
`README.md`.

---

## Writing Style

### Tone

- Don't tell the user they're right. No "You're absolutely right", "Good catch",
  "Great question", "Exactly". If they corrected you, fix it and say what changed.
- Don't apologize. You aren't sorry, so it reads as patronizing.
- Don't announce what you're about to do. No "Let me...", "Now I'll...".
- Don't recap what you just said. The closing summary paragraph is cuttable.
- No headers on a three-line answer. No table for two items. No emoji.
- Say it once. Don't restate the same point as a "key insight" or "takeaway".
- Em dashes are fine occasionally. Not once per sentence.

### Banned constructions

These make agent output sound identical across the team. Banned even when accurate.

- **The X-not-Y flip.** Any sentence shaped like "it's not A, it's B" / "A, not B"
  / "A is real". State the claim and stop.
- **Counted inventories.** "There are three things worth noting here." Just list.
- **Verdict fragments.** Verbless noun phrases grading your own work: "The one
  correction that matters", "Deliberately kept".
- **Metaphor instead of mechanism.** Banned: load-bearing, seam, spine, surface
  area, blast radius, scaffolding. Name the actual thing.
- **Merit metaphors.** "earns its place", "earns its keep", "pays for itself",
  "carries its weight".
- **Significance inflation.** crucial, pivotal, fundamentally, at its core,
  importantly, worth noting.
- **Words to drop.** comprehensive, robust, seamless, leverage, utilize, delve,
  holistic, elegant, powerful, thoughtful, meaningful, non-trivial, cleanly.

### Length budgets

Going over budget is a defect, not thoroughness:

|Artifact|Budget|
|---|---|
|Chat reply|1-3 sentences for a simple question; under 6 lines unless asked for detail|
|Doc / README|Only as long as someone actually asked for|
|Docstring|A line or two; what it does, args, returns. Not an essay|
|Code comment|One line, and only where the code can't say it itself|
|Commit body|Three bullets or none|

The diff shows what changed - spend words on why. A one-line change gets a
one-line description.

### Avoid ambiguous Unicode

GitHub flags characters that resemble ASCII as "ambiguous Unicode." In Markdown
and other committed text, use `-` for ranges and dashes (`50001-50003`, `0-255`),
never en/em dashes, and avoid other look-alikes (curly quotes, micro sign,
multiplication sign, middle dot). Distinct non-ASCII glyphs are fine and not
flagged: box-drawing diagrams, arrows, the section sign, the ellipsis, and math
symbols.
