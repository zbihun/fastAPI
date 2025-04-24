from fastapi import status

from main import app
from routers.users import get_db, get_current_user
from models import Todos, Users

from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["id"] == 1
    assert response_json["email"] == "test"
    assert response_json["username"] == "test"
    assert response_json["first_name"] == "test"
    assert response_json["last_name"] == "test"
    assert response_json["is_active"] is True
    assert response_json["role"] == "admin"
    assert response_json["phone_number"] == "0123456789"

def test_change_password(test_user):
    response = client.put("/user/password", json={"password": "test", "new_password": "new_password"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_password(test_user):
    response = client.put("/user/password", json={"password": "incorrect", "new_password": "new_password"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect password"}

def test_change_phone_number(test_user):
    response = client.put("/user/phone-number", json={"phone_number": "111111111"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
