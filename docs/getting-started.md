# Getting Started

## Run the API

### Docker

```bash
docker build -t hamlib-rest ./
docker run --privileged -p 8080:8080 hamlib-rest
```

### Devcontainer / local Python

```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

## Authenticate

```bash
curl -u admin:password123 -X POST http://localhost:8080/login
```

Use the returned `session_id` for subsequent requests.

## Initialize a rig

```bash
curl -X POST "http://localhost:8080/rig/init?session_id=YOUR_SESSION" \
  -H "Content-Type: application/json" \
  -d '{
    "model": 1,
    "port": "/dev/null",
    "baud": 9600,
    "conf": {
      "ptt_type": "RIG",
      "dcd_type": "RIG"
    }
  }'
```

## Basic examples

```bash
# Get frequency
curl "http://localhost:8080/rig/frequency?session_id=YOUR_SESSION"

# Set frequency
curl -X POST "http://localhost:8080/rig/frequency?session_id=YOUR_SESSION" \
  -H "Content-Type: application/json" \
  -d '{"frequency": 7100000}'

# Get mode
curl "http://localhost:8080/rig/mode?session_id=YOUR_SESSION"

# Set mode
curl -X POST "http://localhost:8080/rig/mode?session_id=YOUR_SESSION" \
  -H "Content-Type: application/json" \
  -d '{"mode": "USB", "width": 2400}'
```

## OpenAPI UI

- Dynamic Swagger UI from backend: `http://localhost:8080/docs`
