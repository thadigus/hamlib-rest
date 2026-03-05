import re
from typing import Dict, List

import Hamlib


_DIGIT_SUFFIX_RE = re.compile(r".*_\d+$")
_BIT_SUFFIX_RE = re.compile(r".*_BIT\d+$")


def _collect_int_constants(
    prefix: str,
    *,
    exclude_names: set[str] | None = None,
    drop_digit_suffix: bool = False,
    drop_bit_suffix: bool = False,
) -> Dict[str, int]:
    constants: Dict[str, int] = {}
    excluded = exclude_names or set()

    for name in sorted(n for n in dir(Hamlib) if n.startswith(prefix)):
        if name in excluded:
            continue
        if drop_digit_suffix and _DIGIT_SUFFIX_RE.match(name):
            continue
        if drop_bit_suffix and _BIT_SUFFIX_RE.match(name):
            continue

        value = getattr(Hamlib, name)
        if isinstance(value, int):
            constants[name] = int(value)

    return constants


GROUP_TO_PREFIX: Dict[str, str] = {
    "mode": "RIG_MODE_",
    "vfo": "RIG_VFO_",
    "level": "RIG_LEVEL_",
    "function": "RIG_FUNC_",
    "parameter": "RIG_PARM_",
    "scan": "RIG_SCAN_",
    "reset": "RIG_RESET_",
    "op": "RIG_OP_",
    "ptt": "RIG_PTT_",
    "power": "RIG_POWER_",
    "trn": "RIG_TRN_",
    "agc": "RIG_AGC_",
    "rptr_shift": "RIG_RPT_SHIFT_",
    "split": "RIG_SPLIT_",
}


GROUP_CONSTANTS: Dict[str, Dict[str, int]] = {
    "mode": _collect_int_constants(
        "RIG_MODE_",
        exclude_names={"RIG_MODE_ALL", "RIG_MODE_TESTS_MAX"},
        drop_bit_suffix=True,
    ),
    "vfo": _collect_int_constants("RIG_VFO_"),
    "level": _collect_int_constants(
        "RIG_LEVEL_",
        exclude_names={"RIG_LEVEL_FLOAT_LIST", "RIG_LEVEL_READONLY_LIST"},
        drop_digit_suffix=True,
    ),
    "function": _collect_int_constants("RIG_FUNC_", drop_bit_suffix=True),
    "parameter": _collect_int_constants("RIG_PARM_"),
    "scan": _collect_int_constants("RIG_SCAN_"),
    "reset": _collect_int_constants("RIG_RESET_"),
    "op": _collect_int_constants("RIG_OP_"),
    "ptt": _collect_int_constants("RIG_PTT_"),
    "power": _collect_int_constants("RIG_POWER_"),
    "trn": _collect_int_constants("RIG_TRN_"),
    "agc": _collect_int_constants("RIG_AGC_"),
    "rptr_shift": _collect_int_constants("RIG_RPT_SHIFT_"),
    "split": _collect_int_constants("RIG_SPLIT_"),
}


GROUP_REVERSE_CONSTANTS: Dict[str, Dict[int, str]] = {}
for group, mapping in GROUP_CONSTANTS.items():
    reverse: Dict[int, str] = {}
    for name in sorted(mapping):
        reverse.setdefault(mapping[name], name)
    GROUP_REVERSE_CONSTANTS[group] = reverse


MODEL_CONSTANTS = _collect_int_constants(
    "RIG_MODEL_",
    exclude_names={"RIG_MODEL_NONE"},
)


def parse_constant(value: str | int, group: str) -> int:
    if group not in GROUP_CONSTANTS:
        raise ValueError(f"Unsupported constant group '{group}'")

    if isinstance(value, int):
        return value

    raw = value.strip()
    if not raw:
        raise ValueError(f"Empty value for group '{group}'")

    try:
        return int(raw, 0)
    except ValueError:
        pass

    mapping = GROUP_CONSTANTS[group]
    upper = raw.upper()

    if upper in mapping:
        return mapping[upper]

    prefix = GROUP_TO_PREFIX[group]
    with_prefix = f"{prefix}{upper}"
    if with_prefix in mapping:
        return mapping[with_prefix]

    raise ValueError(f"Unknown {group} constant '{value}'")


def constant_name(value: int, group: str) -> str:
    if group not in GROUP_REVERSE_CONSTANTS:
        raise ValueError(f"Unsupported constant group '{group}'")
    return GROUP_REVERSE_CONSTANTS[group].get(int(value), str(int(value)))


def decode_bitmask(mask: int, group: str) -> List[str]:
    mapping = GROUP_CONSTANTS[group]
    enabled: List[str] = []
    mask = int(mask)

    for name, value in sorted(mapping.items(), key=lambda item: item[1]):
        if value <= 0:
            continue
        if value & (value - 1):
            continue
        if mask & value:
            enabled.append(name)

    return enabled


def list_models() -> List[dict]:
    models = []
    for name, model_id in sorted(MODEL_CONSTANTS.items(), key=lambda item: item[1]):
        models.append(
            {
                "name": name,
                "model": model_id,
                "label": name.removeprefix("RIG_MODEL_").replace("_", " "),
            }
        )
    return models
