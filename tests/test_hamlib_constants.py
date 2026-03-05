import pytest

from lib.hamlib_constants import (
    GROUP_CONSTANTS,
    constant_name,
    decode_bitmask,
    list_models,
    parse_constant,
)


def test_parse_constant_accepts_prefixed_and_short_names():
    expected = GROUP_CONSTANTS["vfo"]["RIG_VFO_A"]

    assert parse_constant("RIG_VFO_A", "vfo") == expected
    assert parse_constant("A", "vfo") == expected


def test_parse_constant_accepts_numeric_values():
    assert parse_constant("1", "vfo") == 1
    assert parse_constant("0x1", "vfo") == 1


def test_parse_constant_accepts_int_passthrough():
    assert parse_constant(123, "mode") == 123


def test_parse_constant_raises_for_unknown_group():
    with pytest.raises(ValueError):
        parse_constant("RIG_VFO_A", "unknown")


def test_parse_constant_raises_for_unknown_value():
    with pytest.raises(ValueError):
        parse_constant("DOES_NOT_EXIST", "mode")


def test_constant_name_returns_known_symbol_or_fallback_number():
    assert constant_name(1, "vfo") == "RIG_VFO_A"
    assert constant_name(987654321, "vfo") == "987654321"


def test_decode_bitmask_returns_enabled_power_of_two_symbols():
    mask = GROUP_CONSTANTS["function"]["RIG_FUNC_NB"] | GROUP_CONSTANTS["function"]["RIG_FUNC_TONE"]

    decoded = decode_bitmask(mask, "function")

    assert "RIG_FUNC_NB" in decoded
    assert "RIG_FUNC_TONE" in decoded


def test_list_models_returns_items_with_required_keys():
    models = list_models()

    assert models
    first = models[0]
    assert set(first.keys()) == {"name", "model", "label"}
    assert first["name"].startswith("RIG_MODEL_")
