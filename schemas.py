from typing import Any

from pydantic import BaseModel


class InitRigRequest(BaseModel):
    model: int
    port: str | None = None
    baud: int | None = None
    conf: dict[str, Any] = {}


class Frequency(BaseModel):
    frequency: float


class Mode(BaseModel):
    mode: str
    width: int | None = None


class Passband(BaseModel):
    width: int


class LevelChange(BaseModel):
    level: str
    value: float


class FunctionState(BaseModel):
    function: str
    state: int


class ParameterState(BaseModel):
    parameter: str
    value: float


class SplitConfig(BaseModel):
    enabled: bool | None = None
    vfo: str | None = None
    tx_vfo: str | None = None
    tx_freq: float | None = None
    mode: str | None = None
    width: int | None = None


class RIT(BaseModel):
    offset: int


class XIT(BaseModel):
    offset: int


class RepeaterConfig(BaseModel):
    shift: str | None = None
    offset: int | None = None


class PTTState(BaseModel):
    state: Any


class PowerState(BaseModel):
    state: Any


class MemoryChannel(BaseModel):
    channel: int


class MemoryBank(BaseModel):
    bank: int


class ToneValue(BaseModel):
    tone: int


class DCSValue(BaseModel):
    code: int


class TransceiveState(BaseModel):
    state: Any


class TuningStep(BaseModel):
    step: int


class ScanRequest(BaseModel):
    scan: str
    channel: int = 0


class ResetRequest(BaseModel):
    reset: str


class VFOOpRequest(BaseModel):
    op: str


class ConfigRequest(BaseModel):
    name: str
    value: str


class MorseRequest(BaseModel):
    message: str


class DTMFRequest(BaseModel):
    digits: str
