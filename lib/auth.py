# auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from uuid import uuid4
from typing import Dict
import secrets

security = HTTPBasic()

# Simple user store (replace with DB if needed)
VALID_USERS = {
    "admin": "password123",
}

# In-memory session store
sessions: Dict[str, str] = {}  # session_id -> username


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

    # Create a session token
    session_id = str(uuid4())
    sessions[session_id] = credentials.username
    return {"session_id": session_id}


def require_session(session_id: str):
    """Validate session token passed by client."""
    if session_id not in sessions:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    return sessions[session_id]  # return username associated with session
