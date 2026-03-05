# Hamlib REST API Documentation

This project provides an authenticated REST interface to Hamlib rig control, with OpenAPI support.

## Documentation Map

- [Getting Started](getting-started.md)
- [Operations](operations.md)
- [API Commands](API_COMMANDS.md)
- [Architecture](ARCHITECTURE.md)
- [Deployment](DEPLOYMENT.md)

## Scope

The API covers practical `rigctl` workflows over HTTP:

- Frequency, VFO, mode, passband
- Split, RIT, XIT, repeater
- Generic Hamlib levels/functions/parameters
- Memory, CTCSS, DCS
- PTT, power, transceive, tuning step, scan/reset/VFO ops
- Configuration read/write

## OpenAPI

- Local Swagger UI: `http://localhost:8080/docs`
- OpenAPI file in repo: [`openapi.yaml`](../openapi.yaml)

## Source Structure

- `main.py`: FastAPI routes
- `lib/hamlib_driver.py`: Hamlib wrapper logic
- `lib/rig_manager.py`: session-scoped rig lifecycle
- `lib/hamlib_constants.py`: constant/model enumeration helpers
- `schemas.py`: request/response schemas
