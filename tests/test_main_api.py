from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

import main
from lib import auth


class FakeRig:
    def __init__(self):
        self.calls = []

    def _record(self, name, *args, **kwargs):
        self.calls.append((name, args, kwargs))

    def get_frequency(self, vfo=None):
        self._record("get_frequency", vfo=vfo)
        return 145000000.0

    def set_frequency(self, freq, vfo=None):
        self._record("set_frequency", freq, vfo=vfo)

    def get_vfo(self):
        self._record("get_vfo")
        return "RIG_VFO_A"

    def set_vfo(self, vfo):
        self._record("set_vfo", vfo)

    def get_mode(self, vfo=None):
        self._record("get_mode", vfo=vfo)
        return {"mode": "RIG_MODE_FM", "width": 15000}

    def set_mode(self, mode, width=None, vfo=None):
        self._record("set_mode", mode, width=width, vfo=vfo)

    def get_passband(self, vfo=None):
        self._record("get_passband", vfo=vfo)
        return 2400

    def set_passband(self, width, vfo=None):
        self._record("set_passband", width, vfo=vfo)

    def get_level(self, level, vfo=None):
        self._record("get_level", level, vfo=vfo)
        return {"level": level, "value": 42, "value_type": "int"}

    def set_level(self, level, value, vfo=None):
        self._record("set_level", level, value, vfo=vfo)

    def get_func(self, function, vfo=None):
        self._record("get_func", function, vfo=vfo)
        return {"function": function, "state": 1}

    def set_func(self, function, state, vfo=None):
        self._record("set_func", function, state, vfo=vfo)

    def get_parm(self, parameter):
        self._record("get_parm", parameter)
        return {"parameter": parameter, "value": 123, "value_type": "int"}

    def set_parm(self, parameter, value):
        self._record("set_parm", parameter, value)

    def get_split(self, vfo=None):
        self._record("get_split", vfo=vfo)
        return {
            "enabled": True,
            "tx_vfo": "RIG_VFO_B",
            "tx_freq": 146000000.0,
            "mode": "RIG_MODE_USB",
            "width": 2400,
        }

    def set_split(self, tx_freq=None, tx_vfo=None, enabled=None, mode=None, width=None, vfo=None):
        self._record(
            "set_split",
            tx_freq=tx_freq,
            tx_vfo=tx_vfo,
            enabled=enabled,
            mode=mode,
            width=width,
            vfo=vfo,
        )

    def get_rit(self, vfo=None):
        self._record("get_rit", vfo=vfo)
        return 10

    def set_rit(self, offset, vfo=None):
        self._record("set_rit", offset, vfo=vfo)

    def get_xit(self, vfo=None):
        self._record("get_xit", vfo=vfo)
        return -10

    def set_xit(self, offset, vfo=None):
        self._record("set_xit", offset, vfo=vfo)

    def get_rptr(self, vfo=None):
        self._record("get_rptr", vfo=vfo)
        return {"shift": "RIG_RPT_SHIFT_PLUS", "offset": 600000}

    def set_rptr(self, offset=None, shift=None, vfo=None):
        self._record("set_rptr", offset=offset, shift=shift, vfo=vfo)

    def get_ptt(self, vfo=None):
        self._record("get_ptt", vfo=vfo)
        return {"state": "RIG_PTT_OFF", "raw": 0}

    def set_ptt(self, state, vfo=None):
        self._record("set_ptt", state, vfo=vfo)

    def get_power_status(self):
        self._record("get_power_status")
        return {"state": "RIG_POWER_ON", "raw": 1}

    def set_power_status(self, state):
        self._record("set_power_status", state)

    def get_memory_channel(self, vfo=None):
        self._record("get_memory_channel", vfo=vfo)
        return 7

    def set_memory_channel(self, channel, vfo=None):
        self._record("set_memory_channel", channel, vfo=vfo)

    def set_memory_bank(self, bank, vfo=None):
        self._record("set_memory_bank", bank, vfo=vfo)

    def get_ctcss_tone(self, vfo=None):
        self._record("get_ctcss_tone", vfo=vfo)
        return 885

    def set_ctcss_tone(self, tone, vfo=None):
        self._record("set_ctcss_tone", tone, vfo=vfo)

    def get_ctcss_sql(self, vfo=None):
        self._record("get_ctcss_sql", vfo=vfo)
        return 885

    def set_ctcss_sql(self, tone, vfo=None):
        self._record("set_ctcss_sql", tone, vfo=vfo)

    def get_dcs_code(self, vfo=None):
        self._record("get_dcs_code", vfo=vfo)
        return 23

    def set_dcs_code(self, code, vfo=None):
        self._record("set_dcs_code", code, vfo=vfo)

    def get_dcs_sql(self, vfo=None):
        self._record("get_dcs_sql", vfo=vfo)
        return 23

    def set_dcs_sql(self, code, vfo=None):
        self._record("set_dcs_sql", code, vfo=vfo)

    def get_transceive(self):
        self._record("get_transceive")
        return {"state": "RIG_TRN_OFF", "raw": 0}

    def set_transceive(self, state):
        self._record("set_transceive", state)

    def get_tuning_step(self, vfo=None):
        self._record("get_tuning_step", vfo=vfo)
        return 100

    def set_tuning_step(self, step, vfo=None):
        self._record("set_tuning_step", step, vfo=vfo)

    def get_dcd(self, vfo=None):
        self._record("get_dcd", vfo=vfo)
        return 0

    def scan(self, scan, channel, vfo=None):
        self._record("scan", scan, channel, vfo=vfo)

    def reset(self, reset):
        self._record("reset", reset)

    def vfo_op(self, op, vfo=None):
        self._record("vfo_op", op, vfo=vfo)

    def send_dtmf(self, digits):
        self._record("send_dtmf", digits)

    def recv_dtmf(self):
        self._record("recv_dtmf")
        return "123#"

    def send_morse(self, message):
        self._record("send_morse", message)

    def get_conf_params(self):
        self._record("get_conf_params")
        return [{"name": "rig_pathname", "value": "/dev/null"}]

    def get_conf(self, name):
        self._record("get_conf", name)
        return "value"

    def set_conf(self, name, value):
        self._record("set_conf", name, value)

    def get_capabilities(self):
        self._record("get_capabilities")
        return {"model_name": "Dummy"}

    def get_info(self):
        self._record("get_info")
        return "dummy info"


@pytest.fixture
def client():
    return TestClient(main.app)


@pytest.fixture
def session_id():
    sid = "test-session"
    auth.sessions[sid] = "admin"
    return sid


@pytest.fixture
def fake_rig(monkeypatch):
    rig = FakeRig()
    monkeypatch.setattr(main, "get_rig", lambda _sid: rig)
    return rig


def test_login_success_and_failure(client):
    ok = client.post("/login", auth=("admin", "password123"))
    bad = client.post("/login", auth=("admin", "wrong"))

    assert ok.status_code == 200
    assert "session_id" in ok.json()
    assert bad.status_code == 401


def test_protected_route_requires_valid_session(client):
    missing = client.get("/rig/frequency")
    invalid = client.get("/rig/frequency", params={"session_id": "invalid"})

    assert missing.status_code == 422
    assert invalid.status_code == 401


def test_list_usb_devices_and_hamlib_metadata(client, session_id, monkeypatch):
    monkeypatch.setattr(
        main.serial.tools.list_ports,
        "comports",
        lambda: [SimpleNamespace(device="/dev/ttyUSB0", description="USB Serial")],
    )
    monkeypatch.setattr(main.HamlibRig, "models", staticmethod(lambda: [{"name": "RIG_MODEL_DUMMY", "model": 1, "label": "DUMMY"}]))
    monkeypatch.setattr(main.HamlibRig, "constant_groups", staticmethod(lambda: {"mode": {"RIG_MODE_USB": 4}}))

    usb = client.get("/devices/usb", params={"session_id": session_id})
    models = client.get("/hamlib/models", params={"session_id": session_id})
    constants_all = client.get("/hamlib/constants", params={"session_id": session_id})
    constants_mode = client.get("/hamlib/constants", params={"session_id": session_id, "group": "mode"})
    constants_bad = client.get("/hamlib/constants", params={"session_id": session_id, "group": "bad"})

    assert usb.status_code == 200
    assert usb.json() == [{"path": "/dev/ttyUSB0", "description": "USB Serial"}]
    assert models.json()["models"][0]["model"] == 1
    assert constants_all.json()["mode"]["RIG_MODE_USB"] == 4
    assert constants_mode.json() == {"mode": {"RIG_MODE_USB": 4}}
    assert constants_bad.status_code == 404


def test_rig_init_and_close_delegate_to_manager(client, session_id, monkeypatch):
    calls = {}

    def fake_init(**kwargs):
        calls["init"] = kwargs

    def fake_close(sid):
        calls["close"] = sid
        return {"status": "rig closed"}

    monkeypatch.setattr(main, "init_rig_for_session_with_conf", fake_init)
    monkeypatch.setattr(main, "close_rig", fake_close)

    init_resp = client.post(
        "/rig/init",
        params={"session_id": session_id},
        json={"model": 1, "port": "/dev/null", "baud": 9600, "conf": {"ptt_type": "RIG"}},
    )
    close_resp = client.post("/rig/close", params={"session_id": session_id})

    assert init_resp.status_code == 200
    assert close_resp.status_code == 200
    assert calls["init"]["session_id"] == session_id
    assert calls["init"]["model"] == 1
    assert calls["close"] == session_id


def test_frequency_vfo_mode_and_passband_endpoints(client, session_id, fake_rig):
    assert client.get("/rig/frequency", params={"session_id": session_id}).json() == {"frequency": 145000000.0}
    assert client.post(
        "/rig/frequency",
        params={"session_id": session_id, "vfo": "RIG_VFO_B"},
        json={"frequency": 7100000},
    ).json() == {"frequency": 7100000.0, "vfo": "RIG_VFO_B"}

    assert client.get("/rig/vfo", params={"session_id": session_id}).json() == {"vfo": "RIG_VFO_A"}
    assert client.post("/rig/vfo", params={"session_id": session_id, "vfo": "RIG_VFO_B"}).json() == {"vfo": "RIG_VFO_B"}

    assert client.get("/rig/mode", params={"session_id": session_id}).json() == {"mode": "RIG_MODE_FM", "width": 15000}
    assert client.post(
        "/rig/mode",
        params={"session_id": session_id},
        json={"mode": "USB", "width": 2400},
    ).json() == {"status": "ok"}

    assert client.get("/rig/passband", params={"session_id": session_id}).json() == {"width": 2400}
    assert client.post(
        "/rig/passband",
        params={"session_id": session_id},
        json={"width": 3000},
    ).json() == {"status": "ok"}


def test_level_function_and_parameter_endpoints(client, session_id, fake_rig):
    assert client.get(
        "/rig/level", params={"session_id": session_id, "level": "RIG_LEVEL_SQL"}
    ).json()["level"] == "RIG_LEVEL_SQL"
    assert client.post(
        "/rig/level",
        params={"session_id": session_id},
        json={"level": "RIG_LEVEL_SQL", "value": 12},
    ).json() == {"status": "ok"}

    assert client.get(
        "/rig/function", params={"session_id": session_id, "function": "RIG_FUNC_NB"}
    ).json()["state"] == 1
    assert client.post(
        "/rig/function",
        params={"session_id": session_id},
        json={"function": "RIG_FUNC_NB", "state": 0},
    ).json() == {"status": "ok"}

    assert client.get(
        "/rig/parameter", params={"session_id": session_id, "parameter": "RIG_PARM_TIME"}
    ).json()["parameter"] == "RIG_PARM_TIME"
    assert client.post(
        "/rig/parameter",
        params={"session_id": session_id},
        json={"parameter": "RIG_PARM_TIME", "value": 1000},
    ).json() == {"status": "ok"}


def test_split_offsets_and_repeater_endpoints(client, session_id, fake_rig):
    assert client.get("/rig/split", params={"session_id": session_id}).json()["enabled"] is True
    assert client.post(
        "/rig/split",
        params={"session_id": session_id},
        json={"enabled": True, "tx_vfo": "RIG_VFO_B", "tx_freq": 146000000, "mode": "USB", "width": 2400},
    ).json() == {"status": "ok"}

    assert client.get("/rig/rit", params={"session_id": session_id}).json() == {"offset": 10}
    assert client.post("/rig/rit", params={"session_id": session_id}, json={"offset": 20}).json() == {"status": "ok"}

    assert client.get("/rig/xit", params={"session_id": session_id}).json() == {"offset": -10}
    assert client.post("/rig/xit", params={"session_id": session_id}, json={"offset": -20}).json() == {"status": "ok"}

    assert client.get("/rig/repeater", params={"session_id": session_id}).json()["shift"] == "RIG_RPT_SHIFT_PLUS"
    assert client.post(
        "/rig/repeater",
        params={"session_id": session_id},
        json={"shift": "RIG_RPT_SHIFT_MINUS", "offset": 500000},
    ).json() == {"status": "ok"}


def test_ptt_power_memory_tone_and_state_endpoints(client, session_id, fake_rig):
    assert client.get("/rig/ptt", params={"session_id": session_id}).json()["state"] == "RIG_PTT_OFF"
    assert client.post("/rig/ptt", params={"session_id": session_id}, json={"state": "RIG_PTT_ON"}).json() == {"status": "ok"}

    assert client.get("/rig/power", params={"session_id": session_id}).json()["state"] == "RIG_POWER_ON"
    assert client.post("/rig/power", params={"session_id": session_id}, json={"state": "RIG_POWER_OFF"}).json() == {"status": "ok"}

    assert client.get("/rig/memory", params={"session_id": session_id}).json() == {"channel": 7}
    assert client.post("/rig/memory", params={"session_id": session_id}, json={"channel": 9}).json() == {"status": "ok"}
    assert client.post("/rig/memory/bank", params={"session_id": session_id}, json={"bank": 2}).json() == {"status": "ok"}

    assert client.get("/rig/tone/ctcss", params={"session_id": session_id}).json() == {"tone": 885}
    assert client.post("/rig/tone/ctcss", params={"session_id": session_id}, json={"tone": 1000}).json() == {"status": "ok"}
    assert client.get("/rig/tone/ctcss-sql", params={"session_id": session_id}).json() == {"tone": 885}
    assert client.post("/rig/tone/ctcss-sql", params={"session_id": session_id}, json={"tone": 1000}).json() == {"status": "ok"}

    assert client.get("/rig/tone/dcs", params={"session_id": session_id}).json() == {"code": 23}
    assert client.post("/rig/tone/dcs", params={"session_id": session_id}, json={"code": 25}).json() == {"status": "ok"}
    assert client.get("/rig/tone/dcs-sql", params={"session_id": session_id}).json() == {"code": 23}
    assert client.post("/rig/tone/dcs-sql", params={"session_id": session_id}, json={"code": 25}).json() == {"status": "ok"}

    assert client.get("/rig/transceive", params={"session_id": session_id}).json()["state"] == "RIG_TRN_OFF"
    assert client.post("/rig/transceive", params={"session_id": session_id}, json={"state": "RIG_TRN_RIG"}).json() == {"status": "ok"}

    assert client.get("/rig/tuning-step", params={"session_id": session_id}).json() == {"step": 100}
    assert client.post("/rig/tuning-step", params={"session_id": session_id}, json={"step": 50}).json() == {"status": "ok"}

    assert client.get("/rig/dcd", params={"session_id": session_id}).json() == {"dcd": 0}


def test_misc_ops_and_config_endpoints(client, session_id, fake_rig):
    assert client.get("/rig/info", params={"session_id": session_id}).json() == {"info": "dummy info"}
    assert client.get("/rig/capabilities", params={"session_id": session_id}).json() == {"model_name": "Dummy"}

    assert client.post(
        "/rig/scan",
        params={"session_id": session_id},
        json={"scan": "RIG_SCAN_MEM", "channel": 1},
    ).json() == {"status": "ok"}
    assert client.post(
        "/rig/reset",
        params={"session_id": session_id},
        json={"reset": "RIG_RESET_SOFT"},
    ).json() == {"status": "ok"}
    assert client.post(
        "/rig/vfo/op",
        params={"session_id": session_id},
        json={"op": "RIG_OP_UP"},
    ).json() == {"status": "ok"}

    assert client.post(
        "/rig/dtmf/send",
        params={"session_id": session_id},
        json={"digits": "123#"},
    ).json() == {"status": "ok"}
    assert client.get("/rig/dtmf/recv", params={"session_id": session_id}).json() == {"digits": "123#"}

    assert client.post(
        "/rig/morse/send",
        params={"session_id": session_id},
        json={"message": "CQ"},
    ).json() == {"status": "ok"}

    assert client.get("/rig/config/params", params={"session_id": session_id}).json() == {
        "params": [{"name": "rig_pathname", "value": "/dev/null"}]
    }
    assert client.get(
        "/rig/config",
        params={"session_id": session_id, "name": "rig_pathname"},
    ).json() == {"name": "rig_pathname", "value": "value"}
    assert client.post(
        "/rig/config",
        params={"session_id": session_id},
        json={"name": "rig_pathname", "value": "/dev/ttyUSB0"},
    ).json() == {"status": "ok"}


def test_value_and_type_errors_return_http_400(client, session_id, monkeypatch):
    class ValueErrorRig:
        def get_info(self):
            raise ValueError("bad value")

    class TypeErrorRig:
        def get_info(self):
            raise TypeError("bad type")

    monkeypatch.setattr(main, "get_rig", lambda _sid: ValueErrorRig())
    value_resp = client.get("/rig/info", params={"session_id": session_id})

    monkeypatch.setattr(main, "get_rig", lambda _sid: TypeErrorRig())
    type_resp = client.get("/rig/info", params={"session_id": session_id})

    assert value_resp.status_code == 400
    assert value_resp.json() == {"detail": "bad value"}
    assert type_resp.status_code == 400
    assert type_resp.json() == {"detail": "bad type"}
