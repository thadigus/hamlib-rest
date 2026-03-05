# API Command Coverage

This API now covers the practical command families used by `rigctl` workflows.

## Discovery and Session

- `POST /login`
- `GET /devices/usb`
- `GET /hamlib/models`
- `GET /hamlib/constants`

## Rig Lifecycle and Capability

- `POST /rig/init`
- `POST /rig/close`
- `GET /rig/info`
- `GET /rig/capabilities`

## Core Radio Control

- `GET/POST /rig/frequency`
- `GET/POST /rig/vfo`
- `GET/POST /rig/mode`
- `GET/POST /rig/passband`

## Generic Hamlib Flag-Based Controls

- `GET/POST /rig/level`
- `GET/POST /rig/function`
- `GET/POST /rig/parameter`

## Split / Offsets / Repeater

- `GET/POST /rig/split`
- `GET/POST /rig/rit`
- `GET/POST /rig/xit`
- `GET/POST /rig/repeater`

## PTT, Power, Memory

- `GET/POST /rig/ptt`
- `GET/POST /rig/power`
- `GET/POST /rig/memory`
- `POST /rig/memory/bank`

## Tone and Signaling

- `GET/POST /rig/tone/ctcss`
- `GET/POST /rig/tone/ctcss-sql`
- `GET/POST /rig/tone/dcs`
- `GET/POST /rig/tone/dcs-sql`

## Misc Operations

- `GET/POST /rig/transceive`
- `GET/POST /rig/tuning-step`
- `GET /rig/dcd`
- `POST /rig/scan`
- `POST /rig/reset`
- `POST /rig/vfo/op`
- `POST /rig/dtmf/send`
- `GET /rig/dtmf/recv`
- `POST /rig/morse/send`

## Config

- `GET /rig/config/params`
- `GET /rig/config`
- `POST /rig/config`

## Known Binding Limitations

Some pointer-heavy Hamlib functions are not fully usable in this Python binding (for example antenna query/set and split-vfo readback), so the API provides best-effort behavior where required.
