from threading import Lock

from lib.hamlib_driver import HamlibRig

_rigs: dict[str, HamlibRig] = {}
_lock = Lock()


def init_rig_for_session(session_id: str, model: int, port: str, baud: int):
    with _lock:
        existing = _rigs.get(session_id)
        if existing:
            try:
                existing.close()
            except Exception:
                pass

        _rigs[session_id] = HamlibRig(
            rig_model=model,
            rig_port=port,
            baud=baud,
        )


def init_rig_for_session_with_conf(
    session_id: str,
    model: int,
    port: str | None,
    baud: int | None,
    conf: dict | None,
):
    with _lock:
        existing = _rigs.get(session_id)
        if existing:
            try:
                existing.close()
            except Exception:
                pass

        _rigs[session_id] = HamlibRig(
            rig_model=model,
            rig_port=port,
            baud=baud,
            conf=conf,
        )


def get_rig(session_id: str) -> HamlibRig:
    rig = _rigs.get(session_id)
    if rig is None:
        raise ValueError(f"No rig initialized for session '{session_id}'")
    return rig


def close_rig(session_id: str):
    with _lock:
        rig = _rigs.pop(session_id, None)
        if rig:
            try:
                rig.close()
            except Exception:
                pass
            return {"status": "rig closed"}
    return {"status": "no rig for session"}


def close_all_rigs():
    with _lock:
        for rig in _rigs.values():
            try:
                rig.close()
            except Exception:
                pass
        _rigs.clear()
