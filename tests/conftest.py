import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib import auth, rig_manager


@pytest.fixture(autouse=True)
def reset_in_memory_state():
    auth.sessions.clear()
    rig_manager._rigs.clear()
    yield
    auth.sessions.clear()
    rig_manager._rigs.clear()
