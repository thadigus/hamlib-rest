from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
import serial.tools.list_ports

from lib.auth import authenticate, require_session
from lib.hamlib_driver import HamlibRig
from lib.rig_manager import (
    close_all_rigs,
    close_rig,
    get_rig,
    init_rig_for_session_with_conf,
)
from schemas import (
    ConfigRequest,
    DCSValue,
    DTMFRequest,
    Frequency,
    FunctionState,
    InitRigRequest,
    LevelChange,
    MemoryBank,
    MemoryChannel,
    Mode,
    MorseRequest,
    ParameterState,
    Passband,
    PowerState,
    PTTState,
    RepeaterConfig,
    ResetRequest,
    RIT,
    ScanRequest,
    SplitConfig,
    ToneValue,
    TransceiveState,
    TuningStep,
    VFOOpRequest,
    XIT,
)


app = FastAPI(
    title="Hamlib REST API Server",
    version="1.1",
    description="REST API for Hamlib rig control",
)


@app.exception_handler(ValueError)
def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(TypeError)
def type_error_handler(request: Request, exc: TypeError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.post("/login", tags=["Auth"])
def login(session=Depends(authenticate)):
    return session


def get_session_user(session_id: str = Query(...)):
    return require_session(session_id)


@app.get("/devices/usb", tags=["System"], summary="List USB serial devices")
def list_usb_devices(user=Depends(get_session_user)):
    return [
        {"path": p.device, "description": p.description}
        for p in serial.tools.list_ports.comports()
    ]


@app.get("/hamlib/models", tags=["Hamlib"], summary="List known Hamlib rig models")
def list_hamlib_models(user=Depends(get_session_user)):
    return {"models": HamlibRig.models()}


@app.get("/hamlib/constants", tags=["Hamlib"], summary="Enumerate Hamlib constant groups")
def list_hamlib_constants(
    group: str | None = Query(None, description="Optional group filter"),
    user=Depends(get_session_user),
):
    groups = HamlibRig.constant_groups()
    if group is None:
        return groups
    if group not in groups:
        raise HTTPException(status_code=404, detail=f"Unknown constant group '{group}'")
    return {group: groups[group]}


@app.post("/rig/init", tags=["Rig"], summary="Initialize rig connection")
def rig_init(
    req: InitRigRequest,
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    init_rig_for_session_with_conf(
        session_id=session_id,
        model=req.model,
        port=req.port,
        baud=req.baud,
        conf=req.conf,
    )
    return {"status": "rig initialized"}


@app.post("/rig/close", tags=["Rig"], summary="Close rig connection")
def rig_close(session_id: str = Query(...), user=Depends(get_session_user)):
    return close_rig(session_id)


@app.on_event("shutdown")
def shutdown_cleanup():
    close_all_rigs()


@app.get("/rig/info", tags=["Rig"], summary="Get backend rig info string")
def get_rig_info(session_id: str = Query(...), user=Depends(get_session_user)):
    return {"info": get_rig(session_id).get_info()}


@app.get("/rig/capabilities", tags=["Rig"], summary="Get rig capability bitmasks decoded")
def get_rig_capabilities(session_id: str = Query(...), user=Depends(get_session_user)):
    return get_rig(session_id).get_capabilities()


@app.get("/rig/frequency", tags=["Frequency"])
def get_freq(
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return {"frequency": get_rig(session_id).get_frequency(vfo=vfo)}


@app.post("/rig/frequency", tags=["Frequency"])
def set_freq(
    freq: Frequency,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_frequency(freq.frequency, vfo=vfo)
    return {"frequency": freq.frequency, "vfo": vfo or "RIG_VFO_CURR"}


@app.get("/rig/vfo", tags=["VFO"])
def get_vfo(session_id: str = Query(...), user=Depends(get_session_user)):
    return {"vfo": get_rig(session_id).get_vfo()}


@app.post("/rig/vfo", tags=["VFO"])
def set_vfo(
    vfo: str = Query(...),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_vfo(vfo)
    return {"vfo": vfo}


@app.get("/rig/mode", tags=["Mode"])
def get_mode(
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return get_rig(session_id).get_mode(vfo=vfo)


@app.post("/rig/mode", tags=["Mode"])
def set_mode(
    mode: Mode,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_mode(mode=mode.mode, width=mode.width, vfo=vfo)
    return {"status": "ok"}


@app.get("/rig/passband", tags=["Mode"])
def get_passband(
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return {"width": get_rig(session_id).get_passband(vfo=vfo)}


@app.post("/rig/passband", tags=["Mode"])
def set_passband(
    req: Passband,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_passband(width=req.width, vfo=vfo)
    return {"status": "ok"}


@app.get("/rig/level", tags=["Levels"])
def get_level(
    level: str = Query(...),
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return get_rig(session_id).get_level(level, vfo=vfo)


@app.post("/rig/level", tags=["Levels"])
def set_level(
    req: LevelChange,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_level(req.level, req.value, vfo=vfo)
    return {"status": "ok"}


@app.get("/rig/function", tags=["Functions"])
def get_function(
    function: str = Query(...),
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return get_rig(session_id).get_func(function, vfo=vfo)


@app.post("/rig/function", tags=["Functions"])
def set_function(
    req: FunctionState,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_func(req.function, req.state, vfo=vfo)
    return {"status": "ok"}


@app.get("/rig/parameter", tags=["Parameters"])
def get_parameter(
    parameter: str = Query(...),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return get_rig(session_id).get_parm(parameter)


@app.post("/rig/parameter", tags=["Parameters"])
def set_parameter(
    req: ParameterState,
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_parm(req.parameter, req.value)
    return {"status": "ok"}


@app.get("/rig/split", tags=["Split"])
def get_split(
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return get_rig(session_id).get_split(vfo=vfo)


@app.post("/rig/split", tags=["Split"])
def set_split(
    cfg: SplitConfig,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_split(
        tx_freq=cfg.tx_freq,
        tx_vfo=cfg.tx_vfo,
        enabled=cfg.enabled,
        mode=cfg.mode,
        width=cfg.width,
        vfo=vfo,
    )
    return {"status": "ok"}


@app.get("/rig/rit", tags=["RIT"])
def get_rit(
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return {"offset": get_rig(session_id).get_rit(vfo=vfo)}


@app.post("/rig/rit", tags=["RIT"])
def set_rit(
    rit: RIT,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_rit(rit.offset, vfo=vfo)
    return {"status": "ok"}


@app.get("/rig/xit", tags=["XIT"])
def get_xit(
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return {"offset": get_rig(session_id).get_xit(vfo=vfo)}


@app.post("/rig/xit", tags=["XIT"])
def set_xit(
    xit: XIT,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_xit(xit.offset, vfo=vfo)
    return {"status": "ok"}


@app.get("/rig/repeater", tags=["Repeater"])
def get_repeater(
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return get_rig(session_id).get_rptr(vfo=vfo)


@app.post("/rig/repeater", tags=["Repeater"])
def set_repeater(
    cfg: RepeaterConfig,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_rptr(offset=cfg.offset, shift=cfg.shift, vfo=vfo)
    return {"status": "ok"}


@app.get("/rig/ptt", tags=["PTT"])
def get_ptt(
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return get_rig(session_id).get_ptt(vfo=vfo)


@app.post("/rig/ptt", tags=["PTT"])
def set_ptt(
    ptt: PTTState,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_ptt(ptt.state, vfo=vfo)
    return {"status": "ok"}


@app.get("/rig/power", tags=["Power"])
def get_power(session_id: str = Query(...), user=Depends(get_session_user)):
    return get_rig(session_id).get_power_status()


@app.post("/rig/power", tags=["Power"])
def set_power(
    power: PowerState,
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_power_status(power.state)
    return {"status": "ok"}


@app.get("/rig/memory", tags=["Memory"])
def get_memory(
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return {"channel": get_rig(session_id).get_memory_channel(vfo=vfo)}


@app.post("/rig/memory", tags=["Memory"])
def set_memory(
    req: MemoryChannel,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_memory_channel(req.channel, vfo=vfo)
    return {"status": "ok"}


@app.post("/rig/memory/bank", tags=["Memory"])
def set_memory_bank(
    req: MemoryBank,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_memory_bank(req.bank, vfo=vfo)
    return {"status": "ok"}


@app.get("/rig/tone/ctcss", tags=["Tone"])
def get_ctcss_tone(
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return {"tone": get_rig(session_id).get_ctcss_tone(vfo=vfo)}


@app.post("/rig/tone/ctcss", tags=["Tone"])
def set_ctcss_tone(
    req: ToneValue,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_ctcss_tone(req.tone, vfo=vfo)
    return {"status": "ok"}


@app.get("/rig/tone/ctcss-sql", tags=["Tone"])
def get_ctcss_sql(
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return {"tone": get_rig(session_id).get_ctcss_sql(vfo=vfo)}


@app.post("/rig/tone/ctcss-sql", tags=["Tone"])
def set_ctcss_sql(
    req: ToneValue,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_ctcss_sql(req.tone, vfo=vfo)
    return {"status": "ok"}


@app.get("/rig/tone/dcs", tags=["Tone"])
def get_dcs_code(
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return {"code": get_rig(session_id).get_dcs_code(vfo=vfo)}


@app.post("/rig/tone/dcs", tags=["Tone"])
def set_dcs_code(
    req: DCSValue,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_dcs_code(req.code, vfo=vfo)
    return {"status": "ok"}


@app.get("/rig/tone/dcs-sql", tags=["Tone"])
def get_dcs_sql(
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return {"code": get_rig(session_id).get_dcs_sql(vfo=vfo)}


@app.post("/rig/tone/dcs-sql", tags=["Tone"])
def set_dcs_sql(
    req: DCSValue,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_dcs_sql(req.code, vfo=vfo)
    return {"status": "ok"}


@app.get("/rig/transceive", tags=["Rig"])
def get_transceive(session_id: str = Query(...), user=Depends(get_session_user)):
    return get_rig(session_id).get_transceive()


@app.post("/rig/transceive", tags=["Rig"])
def set_transceive(
    req: TransceiveState,
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_transceive(req.state)
    return {"status": "ok"}


@app.get("/rig/tuning-step", tags=["Rig"])
def get_tuning_step(
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return {"step": get_rig(session_id).get_tuning_step(vfo=vfo)}


@app.post("/rig/tuning-step", tags=["Rig"])
def set_tuning_step(
    req: TuningStep,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_tuning_step(req.step, vfo=vfo)
    return {"status": "ok"}


@app.get("/rig/dcd", tags=["Rig"])
def get_dcd(
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return {"dcd": get_rig(session_id).get_dcd(vfo=vfo)}


@app.post("/rig/scan", tags=["Rig"])
def start_scan(
    req: ScanRequest,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).scan(req.scan, req.channel, vfo=vfo)
    return {"status": "ok"}


@app.post("/rig/reset", tags=["Rig"])
def reset_rig(
    req: ResetRequest,
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).reset(req.reset)
    return {"status": "ok"}


@app.post("/rig/vfo/op", tags=["VFO"])
def run_vfo_op(
    req: VFOOpRequest,
    vfo: str | None = Query(None),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).vfo_op(req.op, vfo=vfo)
    return {"status": "ok"}


@app.post("/rig/dtmf/send", tags=["DTMF"])
def send_dtmf(
    req: DTMFRequest,
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).send_dtmf(req.digits)
    return {"status": "ok"}


@app.get("/rig/dtmf/recv", tags=["DTMF"])
def recv_dtmf(session_id: str = Query(...), user=Depends(get_session_user)):
    return {"digits": get_rig(session_id).recv_dtmf()}


@app.post("/rig/morse/send", tags=["Morse"])
def send_morse(
    req: MorseRequest,
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).send_morse(req.message)
    return {"status": "ok"}


@app.get("/rig/config/params", tags=["Configuration"])
def get_config_params(session_id: str = Query(...), user=Depends(get_session_user)):
    return {"params": get_rig(session_id).get_conf_params()}


@app.get("/rig/config", tags=["Configuration"])
def get_config(
    name: str = Query(...),
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    return {"name": name, "value": get_rig(session_id).get_conf(name)}


@app.post("/rig/config", tags=["Configuration"])
def set_config(
    req: ConfigRequest,
    session_id: str = Query(...),
    user=Depends(get_session_user),
):
    get_rig(session_id).set_conf(req.name, req.value)
    return {"status": "ok"}
