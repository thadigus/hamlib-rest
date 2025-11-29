# schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# ==========================================================
# Enums
# ==========================================================

class VFO(str, Enum):
    curr = "RIG_VFO_CURR"
    vfoa = "RIG_VFO_A"
    vfob = "RIG_VFO_B"
    vfo_main = "RIG_VFO_MAIN"
    vfo_sub = "RIG_VFO_SUB"


class RigMode(str, Enum):
    LSB = "LSB"
    USB = "USB"
    CW = "CW"
    CWR = "CWR"
    FM = "FM"
    AM = "AM"
    DIG = "DIG"
    PKT = "PKT"
    RTTY = "RTTY"
    RTTYR = "RTTYR"
    SAM = "SAM"
    DRM = "DRM"


class PTTStateEnum(int, Enum):
    OFF = 0
    ON = 1


class PowerStateEnum(int, Enum):
    OFF = 0
    ON = 1
    STANDBY = 2


# ==========================================================
# Models
# ==========================================================

class InitRigRequest(BaseModel):
    model: int = Field(..., description="Hamlib rig model number")
    port: Optional[str] = Field(None, description="Serial/USB device path")
    baud: Optional[int] = Field(None, description="Baud rate")


class Frequency(BaseModel):
    frequency: float = Field(..., description="Frequency in Hz")


class Mode(BaseModel):
    mode: RigMode = Field(..., description="Operating mode (USB, FM, AM, etc.)")
    width: int = Field(..., description="Filter width")


class LevelChange(BaseModel):
    level_flag: int = Field(..., description="Hamlib RIG_LEVEL_* flag")
    value: float = Field(..., description="Level value")


class SplitConfig(BaseModel):
    tx_freq: Optional[float] = None
    tx_vfo: Optional[str] = None
    mode: Optional[RigMode] = None
    width: Optional[int] = None


class RIT(BaseModel):
    offset: int


class XIT(BaseModel):
    offset: int


class RepeaterConfig(BaseModel):
    shift: Optional[int] = None
    offset: Optional[int] = None


class PTTState(BaseModel):
    state: PTTStateEnum


class PowerState(BaseModel):
    state: PowerStateEnum
