# rig_manager.py
from threading import Lock
from typing import Dict
from lib.hamlib_driver import HamlibRig


_rigs: Dict[str, HamlibRig] = {}
_lock = Lock()


# ---------------------------------------------------------
# Rig Initialization
# ---------------------------------------------------------
def init_rig_for_session(session_id: str, model: int, port: str, baud: int):
    """
    Initialize a rig for a session, closing any existing rig safely.
    """
    with _lock:
        # Close existing rig for session (if exists)
        existing = _rigs.get(session_id)
        if existing:
            try:
                existing.close()
            except Exception:
                pass

        # Create new rig
        _rigs[session_id] = HamlibRig(
            rig_model=model,
            rig_port=port,
            baud=baud
        )


# ---------------------------------------------------------
# Rig Access
# ---------------------------------------------------------
def get_rig(session_id: str) -> HamlibRig:
    rig = _rigs.get(session_id)
    if rig is None:
        raise ValueError(f"No rig initialized for session '{session_id}'")
    return rig


# ---------------------------------------------------------
# Rig Cleanup
# ---------------------------------------------------------
def close_rig(session_id: str):
    """
    Close the rig for a session and remove it from registry.
    """
    with _lock:
        rig = _rigs.pop(session_id, None)
        if rig:
            try:
                rig.close()
            except Exception:
                pass


def close_all_rigs():
    """
    Close ALL rigs. Call this during server shutdown.
    """
    with _lock:
        for rig in _rigs.values():
            try:
                rig.close()
            except Exception:
                pass
        _rigs.clear()
