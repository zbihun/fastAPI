import pytest

from datetime import timedelta
from fastapi import status, HTTPException
from jose import jwt

from main import app
from routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from models import Todos, Users

from .utils import *


app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(username=test_user.username, password="test", db=db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

def test_authenticate_user_non_existent(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(username="incorrect", password="test", db=db)
    assert authenticated_user is False

def test_authenticate_user_wrong_pass(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(username=test_user.username, password="incorrect", db=db)
    assert authenticated_user is False

def test_create_access_token():
    username = "testuser"
    user_id = 1
    role = "admin"
    expires_delta = timedelta(days=1)
    token = create_access_token(username=username, user_id=user_id, role=role, expires_delta=expires_delta)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],options={"verify_signature": False})

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role

@pytest.mark.asyncio
async def test_get_current_user():
    encode = {"sub": "testuser", "id": 1, "role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token=token)
    assert user == {"username": "testuser", "id": 1, "user_role": "admin"}

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as exception:
        await get_current_user(token=token)

    assert exception.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exception.value.detail == "Could not validate credentials"
