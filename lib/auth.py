from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from uuid import uuid4

import secrets

security = HTTPBasic()

VALID_USERS = {
    "admin": "password123",
}

sessions: dict[str, str] = {}


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = credentials.username in VALID_USERS
    correct_password = False

    if correct_username:
        correct_password = secrets.compare_digest(
            credentials.password, VALID_USERS[credentials.username]
        )

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    session_id = str(uuid4())
    sessions[session_id] = credentials.username
    return {"session_id": session_id}


def require_session(session_id: str) -> str:
    if session_id not in sessions:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    return sessions[session_id]
