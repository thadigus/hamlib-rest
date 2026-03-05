# Architecture

## Components

- `main.py`: FastAPI route surface and request validation
- `lib/hamlib_driver.py`: high-level wrapper over Python Hamlib bindings
- `lib/rig_manager.py`: per-session rig lifecycle and concurrency lock
- `lib/hamlib_constants.py`: Hamlib constants and model introspection helpers
- `schemas.py`: request/response data contracts

## Request flow

1. Client authenticates with `POST /login`
2. Session token is passed via `session_id` query parameter
3. `/rig/init` creates a `HamlibRig` instance for that session
4. Route handlers delegate to `HamlibRig` methods
5. Responses are returned as JSON

## Design choices

- Session-scoped rig instances support multi-user access patterns
- Generic constant-based endpoints (`/rig/level`, `/rig/function`, `/rig/parameter`) reduce API churn
- OpenAPI-driven route descriptions support client generation and Swagger UI
