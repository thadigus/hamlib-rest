import pytest
from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

from lib import auth


def test_authenticate_success_creates_session():
    creds = HTTPBasicCredentials(username="admin", password="password123")

    result = auth.authenticate(creds)

    assert "session_id" in result
    assert result["session_id"] in auth.sessions
    assert auth.sessions[result["session_id"]] == "admin"


def test_authenticate_rejects_invalid_username():
    creds = HTTPBasicCredentials(username="nope", password="password123")

    with pytest.raises(HTTPException) as exc:
        auth.authenticate(creds)

    assert exc.value.status_code == 401


def test_authenticate_rejects_invalid_password():
    creds = HTTPBasicCredentials(username="admin", password="bad")

    with pytest.raises(HTTPException) as exc:
        auth.authenticate(creds)

    assert exc.value.status_code == 401


def test_require_session_returns_username_for_valid_session():
    auth.sessions["abc"] = "admin"

    user = auth.require_session("abc")

    assert user == "admin"


def test_require_session_raises_for_invalid_session():
    with pytest.raises(HTTPException) as exc:
        auth.require_session("missing")

    assert exc.value.status_code == 401
