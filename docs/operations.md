# Operations

This section summarizes endpoint families and command coverage.

## Discovery and lifecycle

- `POST /login`
- `GET /devices/usb`
- `POST /rig/init`
- `POST /rig/close`
- `GET /rig/info`
- `GET /rig/capabilities`
- `GET /hamlib/models`
- `GET /hamlib/constants`

## Control plane

- `GET/POST /rig/frequency`
- `GET/POST /rig/vfo`
- `GET/POST /rig/mode`
- `GET/POST /rig/passband`
- `GET/POST /rig/split`
- `GET/POST /rig/rit`
- `GET/POST /rig/xit`
- `GET/POST /rig/repeater`

## Generic Hamlib access

- `GET/POST /rig/level` using `RIG_LEVEL_*`
- `GET/POST /rig/function` using `RIG_FUNC_*`
- `GET/POST /rig/parameter` using `RIG_PARM_*`

## Memory, tone, and utility

- `GET/POST /rig/memory`
- `POST /rig/memory/bank`
- `GET/POST /rig/tone/ctcss`
- `GET/POST /rig/tone/ctcss-sql`
- `GET/POST /rig/tone/dcs`
- `GET/POST /rig/tone/dcs-sql`
- `GET/POST /rig/transceive`
- `GET/POST /rig/tuning-step`
- `GET /rig/dcd`
- `POST /rig/scan`
- `POST /rig/reset`
- `POST /rig/vfo/op`
- `POST /rig/dtmf/send`
- `GET /rig/dtmf/recv`
- `POST /rig/morse/send`

## Configuration

- `GET /rig/config/params`
- `GET /rig/config`
- `POST /rig/config`

For the detailed command list, see [API_COMMANDS.md](API_COMMANDS.md).
