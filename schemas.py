from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class InitRigRequest(BaseModel):
    model: int = Field(..., description="Hamlib rig model number")
    port: Optional[str] = Field(None, description="Serial/USB/TCP rig path")
    baud: Optional[int] = Field(None, description="Serial baud rate")
    conf: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional backend config parameters to apply on init",
    )


class Frequency(BaseModel):
    frequency: float = Field(..., description="Frequency in Hz")


class Mode(BaseModel):
    mode: str = Field(..., description="Mode name, e.g. USB or RIG_MODE_USB")
    width: Optional[int] = Field(None, description="Filter width / passband in Hz")


class Passband(BaseModel):
    width: int = Field(..., description="Passband width in Hz")


class LevelChange(BaseModel):
    level: str = Field(..., description="Level constant name, e.g. RIG_LEVEL_SQL")
    value: float = Field(..., description="Level value")


class FunctionState(BaseModel):
    function: str = Field(..., description="Function constant name, e.g. RIG_FUNC_NB")
    state: int = Field(..., description="0 or 1")


class ParameterState(BaseModel):
    parameter: str = Field(..., description="Parameter constant name, e.g. RIG_PARM_TIME")
    value: float = Field(..., description="Parameter value")


class SplitConfig(BaseModel):
    enabled: Optional[bool] = Field(None, description="Split on/off")
    tx_freq: Optional[float] = Field(None, description="TX frequency in Hz")
    tx_vfo: Optional[str] = Field(None, description="TX VFO name")
    mode: Optional[str] = Field(None, description="TX mode")
    width: Optional[int] = Field(None, description="TX passband width in Hz")


class RIT(BaseModel):
    offset: int = Field(..., description="RIT offset in Hz")


class XIT(BaseModel):
    offset: int = Field(..., description="XIT offset in Hz")


class RepeaterConfig(BaseModel):
    shift: Optional[str] = Field(None, description="RIG_RPT_SHIFT_* value")
    offset: Optional[int] = Field(None, description="Repeater offset in Hz")


class PTTState(BaseModel):
    state: Any = Field(..., description="PTT state (bool/int/name)")


class PowerState(BaseModel):
    state: Any = Field(..., description="Power state (int/name)")


class MemoryChannel(BaseModel):
    channel: int = Field(..., description="Memory channel number")


class MemoryBank(BaseModel):
    bank: int = Field(..., description="Memory bank number")


class ToneValue(BaseModel):
    tone: int = Field(..., description="Tone value")


class DCSValue(BaseModel):
    code: int = Field(..., description="DCS code")


class TransceiveState(BaseModel):
    state: Any = Field(..., description="Transceive mode")


class TuningStep(BaseModel):
    step: int = Field(..., description="Tuning step in Hz")


class ScanRequest(BaseModel):
    scan: str = Field(..., description="Scan type, e.g. RIG_SCAN_MEM")
    channel: int = Field(0, description="Optional channel index")


class ResetRequest(BaseModel):
    reset: str = Field(..., description="Reset type, e.g. RIG_RESET_SOFT")


class VFOOpRequest(BaseModel):
    op: str = Field(..., description="VFO operation, e.g. RIG_OP_UP")


class ConfigRequest(BaseModel):
    name: str = Field(..., description="Config key")
    value: str = Field(..., description="Config value")


class MorseRequest(BaseModel):
    message: str = Field(..., description="Morse text to send")


class DTMFRequest(BaseModel):
    digits: str = Field(..., description="DTMF digits to send")
