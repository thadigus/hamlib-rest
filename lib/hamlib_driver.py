from __future__ import annotations

from typing import Any

import Hamlib

from lib.hamlib_constants import (
    GROUP_CONSTANTS,
    constant_name,
    decode_bitmask,
    list_models,
    parse_constant,
)


class HamlibRig:
    KNOWN_CONF_PARAMS = [
        "rig_pathname",
        "serial_speed",
        "data_bits",
        "stop_bits",
        "parity",
        "handshake",
        "retry",
        "timeout",
        "write_delay",
        "post_write_delay",
        "ptt_type",
        "ptt_pathname",
        "dcd_type",
        "dcd_pathname",
        "civaddr",
    ]

    def __init__(
        self,
        rig_model: int,
        rig_port: str | None = None,
        baud: int | None = None,
        conf: dict[str, Any] | None = None,
    ):
        Hamlib.rig_set_debug(Hamlib.RIG_DEBUG_NONE)

        self.rig = Hamlib.Rig(rig_model)
        self._split_enabled: bool | None = None
        self._split_tx_vfo: str | None = None

        if rig_port:
            self.rig.set_conf("rig_pathname", rig_port)
        if baud:
            self.rig.set_conf("serial_speed", str(baud))
        if conf:
            for key, value in conf.items():
                self.rig.set_conf(str(key), str(value))

        self.rig.open()

    def close(self):
        self.rig.close()

    @staticmethod
    def constant_groups() -> dict[str, dict[str, int]]:
        return GROUP_CONSTANTS

    @staticmethod
    def models() -> list[dict[str, Any]]:
        return list_models()

    def _resolve_vfo(self, vfo: str | int | None = None) -> int:
        if vfo is None:
            return Hamlib.RIG_VFO_CURR
        return parse_constant(vfo, "vfo")

    def _resolve_mode(self, mode: str | int) -> int:
        return parse_constant(mode, "mode")

    def _resolve_level(self, level: str | int) -> int:
        return parse_constant(level, "level")

    def _resolve_func(self, func: str | int) -> int:
        return parse_constant(func, "function")

    def _resolve_parm(self, parm: str | int) -> int:
        return parse_constant(parm, "parameter")

    def get_frequency(self, vfo: str | int | None = None) -> float:
        return float(self.rig.get_freq(self._resolve_vfo(vfo)))

    def set_frequency(self, freq: float, vfo: str | int | None = None):
        self.rig.set_freq(self._resolve_vfo(vfo), float(freq))

    def get_vfo(self) -> str:
        return constant_name(int(self.rig.get_vfo()), "vfo")

    def set_vfo(self, vfo: str | int):
        self.rig.set_vfo(self._resolve_vfo(vfo))

    def get_mode(self, vfo: str | int | None = None) -> dict[str, Any]:
        mode, width = self.rig.get_mode(self._resolve_vfo(vfo))
        return {"mode": constant_name(int(mode), "mode"), "width": int(width)}

    def set_mode(
        self,
        mode: str | int,
        width: int | None = None,
        vfo: str | int | None = None,
    ):
        target_vfo = self._resolve_vfo(vfo)
        target_mode = self._resolve_mode(mode)

        if width is None:
            _, current_width = self.rig.get_mode(target_vfo)
            width = int(current_width)

        self.rig.set_mode(target_vfo, target_mode, int(width))

    def get_passband(self, vfo: str | int | None = None) -> int:
        return int(self.get_mode(vfo)["width"])

    def set_passband(self, width: int, vfo: str | int | None = None):
        target_vfo = self._resolve_vfo(vfo)
        current_mode, _ = self.rig.get_mode(target_vfo)
        self.rig.set_mode(target_vfo, int(current_mode), int(width))

    def get_level(self, level_flag: str | int, vfo: str | int | None = None) -> dict[str, Any]:
        flag = self._resolve_level(level_flag)
        target_vfo = self._resolve_vfo(vfo)

        if flag & Hamlib.RIG_LEVEL_FLOAT_LIST:
            value = float(self.rig.get_level_f(flag, target_vfo))
            value_type = "float"
        else:
            value = int(self.rig.get_level_i(flag, target_vfo))
            value_type = "int"

        return {
            "level": constant_name(flag, "level"),
            "value": value,
            "value_type": value_type,
        }

    def set_level(
        self,
        level_flag: str | int,
        value: float | int,
        vfo: str | int | None = None,
    ):
        flag = self._resolve_level(level_flag)
        target_vfo = self._resolve_vfo(vfo)

        if flag & Hamlib.RIG_LEVEL_FLOAT_LIST:
            self.rig.set_level(flag, float(value), target_vfo)
        else:
            self.rig.set_level(flag, int(value), target_vfo)

    def get_func(self, func_flag: str | int, vfo: str | int | None = None) -> dict[str, Any]:
        flag = self._resolve_func(func_flag)
        state = int(self.rig.get_func(self._resolve_vfo(vfo), flag))
        return {
            "function": constant_name(flag, "function"),
            "state": state,
        }

    def set_func(
        self,
        func_flag: str | int,
        state: bool | int,
        vfo: str | int | None = None,
    ):
        self.rig.set_func(
            self._resolve_vfo(vfo),
            self._resolve_func(func_flag),
            int(bool(state)),
        )

    def get_parm(self, parm_flag: str | int) -> dict[str, Any]:
        flag = self._resolve_parm(parm_flag)

        if flag == getattr(Hamlib, "RIG_PARM_BAT", -1):
            value = float(self.rig.get_parm_f(flag))
            value_type = "float"
        else:
            value = int(self.rig.get_parm_i(flag))
            value_type = "int"

        return {
            "parameter": constant_name(flag, "parameter"),
            "value": value,
            "value_type": value_type,
        }

    def set_parm(self, parm_flag: str | int, value: float | int):
        flag = self._resolve_parm(parm_flag)

        if flag == getattr(Hamlib, "RIG_PARM_BAT", -1):
            self.rig.set_parm(flag, float(value))
        else:
            self.rig.set_parm(flag, int(value))

    def get_split(self, vfo: str | int | None = None) -> dict[str, Any]:
        target_vfo = self._resolve_vfo(vfo)
        tx_mode, tx_width = self.rig.get_split_mode(target_vfo)
        tx_freq = self.rig.get_split_freq(target_vfo)

        return {
            "enabled": self._split_enabled,
            "tx_vfo": self._split_tx_vfo,
            "tx_freq": float(tx_freq),
            "mode": constant_name(int(tx_mode), "mode"),
            "width": int(tx_width),
        }

    def set_split(
        self,
        tx_freq: float | None = None,
        tx_vfo: str | int | None = None,
        enabled: bool | None = None,
        mode: str | int | None = None,
        width: int | None = None,
        vfo: str | int | None = None,
    ):
        target_vfo = self._resolve_vfo(vfo)

        if tx_freq is not None:
            self.rig.set_split_freq(target_vfo, float(tx_freq))

        if tx_vfo is not None or enabled is not None:
            split_flag = Hamlib.RIG_SPLIT_ON if bool(enabled) else Hamlib.RIG_SPLIT_OFF
            if enabled is None:
                split_flag = Hamlib.RIG_SPLIT_ON

            split_tx_vfo = self._resolve_vfo(tx_vfo or self._split_tx_vfo or "B")
            self.rig.set_split_vfo(target_vfo, split_flag, split_tx_vfo)
            self._split_enabled = bool(split_flag == Hamlib.RIG_SPLIT_ON)
            self._split_tx_vfo = constant_name(split_tx_vfo, "vfo")

        if mode is not None:
            target_mode = self._resolve_mode(mode)
            if width is None:
                _, current_width = self.rig.get_split_mode(target_vfo)
                width = int(current_width)
            self.rig.set_split_mode(target_vfo, target_mode, int(width))

    def get_rit(self, vfo: str | int | None = None) -> int:
        return int(self.rig.get_rit(self._resolve_vfo(vfo)))

    def set_rit(self, offset: int, vfo: str | int | None = None):
        self.rig.set_rit(self._resolve_vfo(vfo), int(offset))

    def get_xit(self, vfo: str | int | None = None) -> int:
        return int(self.rig.get_xit(self._resolve_vfo(vfo)))

    def set_xit(self, offset: int, vfo: str | int | None = None):
        self.rig.set_xit(self._resolve_vfo(vfo), int(offset))

    def get_rptr(self, vfo: str | int | None = None) -> dict[str, Any]:
        target_vfo = self._resolve_vfo(vfo)
        shift = int(self.rig.get_rptr_shift(target_vfo))
        offset = int(self.rig.get_rptr_offs(target_vfo))
        return {
            "shift": constant_name(shift, "rptr_shift"),
            "offset": offset,
        }

    def set_rptr(
        self,
        offset: int | None = None,
        shift: str | int | None = None,
        vfo: str | int | None = None,
    ):
        target_vfo = self._resolve_vfo(vfo)
        if offset is not None:
            self.rig.set_rptr_offs(target_vfo, int(offset))
        if shift is not None:
            self.rig.set_rptr_shift(target_vfo, parse_constant(shift, "rptr_shift"))

    def get_ptt(self, vfo: str | int | None = None) -> dict[str, Any]:
        state = int(self.rig.get_ptt(self._resolve_vfo(vfo)))
        return {
            "state": constant_name(state, "ptt"),
            "raw": state,
        }

    def set_ptt(self, ptt_state: str | int | bool, vfo: str | int | None = None):
        if isinstance(ptt_state, bool):
            state = Hamlib.RIG_PTT_ON if ptt_state else Hamlib.RIG_PTT_OFF
        else:
            state = parse_constant(ptt_state, "ptt")
        self.rig.set_ptt(self._resolve_vfo(vfo), state)

    def get_power_status(self) -> dict[str, Any]:
        state = int(self.rig.get_powerstat())
        return {
            "state": constant_name(state, "power"),
            "raw": state,
        }

    def set_power_status(self, status: str | int):
        self.rig.set_powerstat(parse_constant(status, "power"))

    def get_memory_channel(self, vfo: str | int | None = None) -> int:
        return int(self.rig.get_mem(self._resolve_vfo(vfo)))

    def set_memory_channel(self, channel: int, vfo: str | int | None = None):
        self.rig.set_mem(self._resolve_vfo(vfo), int(channel))

    def set_memory_bank(self, bank: int, vfo: str | int | None = None):
        self.rig.set_bank(self._resolve_vfo(vfo), int(bank))

    def get_ctcss_tone(self, vfo: str | int | None = None) -> int:
        return int(self.rig.get_ctcss_tone(self._resolve_vfo(vfo)))

    def set_ctcss_tone(self, tone: int, vfo: str | int | None = None):
        self.rig.set_ctcss_tone(self._resolve_vfo(vfo), int(tone))

    def get_ctcss_sql(self, vfo: str | int | None = None) -> int:
        return int(self.rig.get_ctcss_sql(self._resolve_vfo(vfo)))

    def set_ctcss_sql(self, tone: int, vfo: str | int | None = None):
        self.rig.set_ctcss_sql(self._resolve_vfo(vfo), int(tone))

    def get_dcs_code(self, vfo: str | int | None = None) -> int:
        return int(self.rig.get_dcs_code(self._resolve_vfo(vfo)))

    def set_dcs_code(self, code: int, vfo: str | int | None = None):
        self.rig.set_dcs_code(self._resolve_vfo(vfo), int(code))

    def get_dcs_sql(self, vfo: str | int | None = None) -> int:
        return int(self.rig.get_dcs_sql(self._resolve_vfo(vfo)))

    def set_dcs_sql(self, code: int, vfo: str | int | None = None):
        self.rig.set_dcs_sql(self._resolve_vfo(vfo), int(code))

    def get_transceive(self) -> dict[str, Any]:
        state = int(self.rig.get_trn())
        return {
            "state": constant_name(state, "trn"),
            "raw": state,
        }

    def set_transceive(self, state: str | int):
        self.rig.set_trn(parse_constant(state, "trn"))

    def get_tuning_step(self, vfo: str | int | None = None) -> int:
        return int(self.rig.get_ts(self._resolve_vfo(vfo)))

    def set_tuning_step(self, step_hz: int, vfo: str | int | None = None):
        self.rig.set_ts(self._resolve_vfo(vfo), int(step_hz))

    def get_dcd(self, vfo: str | int | None = None) -> int:
        return int(self.rig.get_dcd(self._resolve_vfo(vfo)))

    def scan(self, scan_type: str | int, channel: int = 0, vfo: str | int | None = None):
        self.rig.scan(
            self._resolve_vfo(vfo),
            parse_constant(scan_type, "scan"),
            int(channel),
        )

    def reset(self, reset_type: str | int):
        self.rig.reset(parse_constant(reset_type, "reset"))

    def vfo_op(self, op: str | int, vfo: str | int | None = None):
        self.rig.vfo_op(self._resolve_vfo(vfo), parse_constant(op, "op"))

    def send_dtmf(self, digits: str):
        self.rig.send_dtmf(digits)

    def recv_dtmf(self) -> str:
        return str(self.rig.recv_dtmf())

    def send_morse(self, message: str):
        self.rig.send_morse(message)

    def get_info(self) -> str:
        return str(self.rig.get_info())

    def set_conf(self, name: str, value: str):
        self.rig.set_conf(name, value)

    def get_conf(self, name: str) -> str:
        return str(self.rig.get_conf(name))

    def get_conf_params(self) -> list[dict[str, str]]:
        params: list[dict[str, str]] = []
        for name in self.KNOWN_CONF_PARAMS:
            try:
                params.append({"name": name, "value": self.get_conf(name)})
            except Exception:
                continue
        return params

    def get_capabilities(self) -> dict[str, Any]:
        caps = self.rig.caps
        return {
            "rig_model": int(caps.rig_model),
            "model_name": str(caps.model_name),
            "mfg_name": str(caps.mfg_name),
            "version": str(caps.version),
            "status": int(caps.status),
            "port_type": int(caps.port_type),
            "ptt_type": int(caps.ptt_type),
            "targetable_vfo": int(caps.targetable_vfo),
            "has_get_level": decode_bitmask(int(caps.has_get_level), "level"),
            "has_set_level": decode_bitmask(int(caps.has_set_level), "level"),
            "has_get_func": decode_bitmask(int(caps.has_get_func), "function"),
            "has_set_func": decode_bitmask(int(caps.has_set_func), "function"),
            "has_get_parm": decode_bitmask(int(caps.has_get_parm), "parameter"),
            "has_set_parm": decode_bitmask(int(caps.has_set_parm), "parameter"),
            "scan_ops": decode_bitmask(int(caps.scan_ops), "scan"),
            "vfo_ops": decode_bitmask(int(caps.vfo_ops), "op"),
        }
