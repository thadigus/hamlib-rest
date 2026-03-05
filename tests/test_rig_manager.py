import pytest

from lib import rig_manager


class DummyRig:
    instances = []

    def __init__(self, rig_model, rig_port=None, baud=None, conf=None):
        self.rig_model = rig_model
        self.rig_port = rig_port
        self.baud = baud
        self.conf = conf
        self.closed = False
        DummyRig.instances.append(self)

    def close(self):
        self.closed = True


@pytest.fixture(autouse=True)
def clear_instances():
    DummyRig.instances = []
    rig_manager._rigs.clear()
    yield
    DummyRig.instances = []
    rig_manager._rigs.clear()


def test_init_rig_for_session_creates_rig(monkeypatch):
    monkeypatch.setattr(rig_manager, "HamlibRig", DummyRig)

    rig_manager.init_rig_for_session("s1", 123, "/dev/ttyUSB0", 9600)

    rig = rig_manager.get_rig("s1")
    assert isinstance(rig, DummyRig)
    assert rig.rig_model == 123
    assert rig.rig_port == "/dev/ttyUSB0"
    assert rig.baud == 9600


def test_init_rig_for_session_replaces_and_closes_existing(monkeypatch):
    monkeypatch.setattr(rig_manager, "HamlibRig", DummyRig)

    rig_manager.init_rig_for_session("s1", 111, "/dev/ttyUSB0", 4800)
    old = rig_manager.get_rig("s1")

    rig_manager.init_rig_for_session("s1", 222, "/dev/ttyUSB1", 9600)
    new = rig_manager.get_rig("s1")

    assert old.closed is True
    assert new is not old
    assert new.rig_model == 222


def test_init_rig_for_session_with_conf_passes_conf(monkeypatch):
    monkeypatch.setattr(rig_manager, "HamlibRig", DummyRig)

    rig_manager.init_rig_for_session_with_conf(
        "s1",
        model=77,
        port="/dev/null",
        baud=19200,
        conf={"ptt_type": "RIG"},
    )

    rig = rig_manager.get_rig("s1")
    assert rig.conf == {"ptt_type": "RIG"}


def test_get_rig_raises_for_missing_session():
    with pytest.raises(ValueError):
        rig_manager.get_rig("missing")


def test_close_rig_returns_closed_status_when_present(monkeypatch):
    monkeypatch.setattr(rig_manager, "HamlibRig", DummyRig)
    rig_manager.init_rig_for_session("s1", 1, "/dev/null", 9600)

    response = rig_manager.close_rig("s1")

    assert response == {"status": "rig closed"}
    assert "s1" not in rig_manager._rigs


def test_close_rig_returns_missing_status_when_not_present():
    response = rig_manager.close_rig("missing")

    assert response == {"status": "no rig for session"}


def test_close_all_rigs_closes_everything(monkeypatch):
    monkeypatch.setattr(rig_manager, "HamlibRig", DummyRig)
    rig_manager.init_rig_for_session("s1", 1, "/dev/null", 9600)
    rig_manager.init_rig_for_session("s2", 2, "/dev/null", 9600)

    created = list(DummyRig.instances)
    rig_manager.close_all_rigs()

    assert all(r.closed for r in created)
    assert rig_manager._rigs == {}
