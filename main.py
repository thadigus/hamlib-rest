# main.py
from fastapi import FastAPI, Depends, Query
from lib.auth import authenticate, require_session
from lib.rig_manager import init_rig_for_session, get_rig
from schemas import (
    InitRigRequest, Frequency, Mode, LevelChange,
    SplitConfig, RIT, XIT, RepeaterConfig,
    PTTState, PowerState
)
import serial.tools.list_ports

app = FastAPI(
    title="Hamlib REST API Server",
    version="1.0",
    description="REST API for Hamlib rig control",
)

# --------------------------
# Authentication
# --------------------------
@app.post("/login", tags=["Auth"])
def login(session=Depends(authenticate)):
    return session

def get_session_user(session_id: str = Query(...)):
    return require_session(session_id)


# --------------------------
# USB Device Discovery
# --------------------------
@app.get("/devices/usb", tags=["System"], summary="List USB serial devices")
def list_usb_devices(user=Depends(get_session_user)):
    return [
        {"path": p.device, "description": p.description}
        for p in serial.tools.list_ports.comports()
    ]


# --------------------------
# Rig Initialization
# --------------------------
@app.post("/rig/init", tags=["Rig"], summary="Initialize rig connection")
def rig_init(req: InitRigRequest, session_id: str = Query(...), user=Depends(get_session_user)):
    init_rig_for_session(
        session_id=session_id,
        model=req.model,
        port=req.port,
        baud=req.baud
    )
    return {"status": "rig initialized"}

# --------------------------
# Close Rig
# --------------------------
@app.post("/rig/close", tags={"Rig"}, summary="")
def rig_close(session_id: str = Query(...), user=Depends(get_session_user)):
    return get_rig(session_id).close_rig()

# --------------------------
# Program Shutdown
# --------------------------
@app.on_event("shutdown")
def shutdown_cleanup():
    close_all_rigs()


# ==========================================================
# Rig Commands
# ==========================================================

# --------------------------
# Frequency
# --------------------------
@app.get("/rig/frequency", response_model=Frequency, tags=["Frequency"])
def get_freq(session_id: str = Query(...), user=Depends(get_session_user)):
    return Frequency(frequency=get_rig(session_id).get_frequency())


@app.post("/rig/frequency", response_model=Frequency, tags=["Frequency"])
def set_freq(freq: Frequency, session_id: str = Query(...), user=Depends(get_session_user)):
    get_rig(session_id).set_frequency(freq.frequency)
    return freq


# --------------------------
# VFO
# --------------------------
@app.get("/rig/vfo", tags=["VFO"])
def get_vfo(session_id: str = Query(...), user=Depends(get_session_user)):
    return {"vfo": get_rig(session_id).get_vfo()}


@app.post("/rig/vfo", tags=["VFO"])
def set_vfo(vfo: str = Query(...), session_id: str = Query(...), user=Depends(get_session_user)):
    get_rig(session_id).set_vfo(vfo)
    return {"vfo": vfo}


# --------------------------
# Mode
# --------------------------
@app.get("/rig/mode", response_model=Mode, tags=["Mode"])
def get_mode(session_id: str = Query(...), user=Depends(get_session_user)):
    m = get_rig(session_id).get_mode()
    return Mode(mode=m["mode"], width=m["width"])


@app.post("/rig/mode", response_model=Mode, tags=["Mode"])
def set_mode(mode: Mode, session_id: str = Query(...), user=Depends(get_session_user)):
    get_rig(session_id).set_mode(mode.mode, mode.width)
    return mode


# --------------------------
# Level
# --------------------------
@app.get("/rig/level", tags=["Levels"])
def get_level(level_flag: int = Query(...), session_id: str = Query(...), user=Depends(get_session_user)):
    value = get_rig(session_id).get_level(level_flag)
    return {"level_flag": level_flag, "value": value}


@app.post("/rig/level", tags=["Levels"])
def set_level(level: LevelChange, session_id: str = Query(...), user=Depends(get_session_user)):
    get_rig(session_id).set_level(level.level_flag, level.value)
    return {"status": "ok"}


# --------------------------
# Split
# --------------------------
@app.get("/rig/split", response_model=SplitConfig, tags=["Split"])
def get_split(session_id: str = Query(...), user=Depends(get_session_user)):
    return SplitConfig(**get_rig(session_id).get_split())


@app.post("/rig/split", tags=["Split"])
def set_split(cfg: SplitConfig, session_id: str = Query(...), user=Depends(get_session_user)):
    get_rig(session_id).set_split(
        tx_freq=cfg.tx_freq,
        tx_vfo=cfg.tx_vfo,
        mode=cfg.mode,
        width=cfg.width
    )
    return {"status": "ok"}


# --------------------------
# RIT / XIT
# --------------------------
@app.get("/rig/rit", response_model=RIT, tags=["RIT"])
def get_rit(session_id: str = Query(...), user=Depends(get_session_user)):
    return RIT(offset=get_rig(session_id).get_rit())


@app.post("/rig/rit", tags=["RIT"])
def set_rit(rit: RIT, session_id: str = Query(...), user=Depends(get_session_user)):
    get_rig(session_id).set_rit(rit.offset)
    return {"status": "ok"}


@app.get("/rig/xit", response_model=XIT, tags=["XIT"])
def get_xit(session_id: str = Query(...), user=Depends(get_session_user)):
    return XIT(offset=get_rig(session_id).get_xit())


@app.post("/rig/xit", tags=["XIT"])
def set_xit(xit: XIT, session_id: str = Query(...), user=Depends(get_session_user)):
    get_rig(session_id).set_xit(xit.offset)
    return {"status": "ok"}


# --------------------------
# Repeater
# --------------------------
@app.get("/rig/repeater", response_model=RepeaterConfig, tags=["Repeater"])
def get_repeater(session_id: str = Query(...), user=Depends(get_session_user)):
    return RepeaterConfig(**get_rig(session_id).get_rptr())


@app.post("/rig/repeater", tags=["Repeater"])
def set_repeater(cfg: RepeaterConfig, session_id: str = Query(...), user=Depends(get_session_user)):
    get_rig(session_id).set_rptr(offset=cfg.offset, shift=cfg.shift)
    return {"status": "ok"}


# --------------------------
# PTT
# --------------------------
@app.get("/rig/ptt", response_model=PTTState, tags=["PTT"])
def get_ptt(session_id: str = Query(...), user=Depends(get_session_user)):
    return PTTState(state=get_rig(session_id).get_ptt())


@app.post("/rig/ptt", tags=["PTT"])
def set_ptt(ptt: PTTState, session_id: str = Query(...), user=Depends(get_session_user)):
    get_rig(session_id).set_ptt(ptt.state)
    return {"status": "ok"}


# --------------------------
# Power
# --------------------------
@app.get("/rig/power", response_model=PowerState, tags=["Power"])
def get_power(session_id: str = Query(...), user=Depends(get_session_user)):
    return PowerState(state=get_rig(session_id).get_power_status())


@app.post("/rig/power", tags=["Power"])
def set_power(power: PowerState, session_id: str = Query(...), user=Depends(get_session_user)):
    get_rig(session_id).set_power_status(power.state)
    return {"status": "ok"}


# --------------------------
# Config Params
# --------------------------
@app.get("/rig/config/params", tags=["Configuration"])
def get_config_params(session_id: str = Query(...), user=Depends(get_session_user)):
    return {"params": get_rig(session_id).get_conf_params()}


@app.post("/rig/config", tags=["Configuration"])
def set_config(
    name: str = Query(...),
    value: str = Query(...),
    session_id: str = Query(...),
    user=Depends(get_session_user)
):
    get_rig(session_id).set_conf(name, value)
    return {"status": "ok"}
