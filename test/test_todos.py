
from fastapi import status

from main import app
from routers.todos import get_db, get_current_user
from models import Todos

from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"complete": False, "title": "Learn to code", "description": "Need to learn", "id": 1, "priority": 5, "owner_id": 1}]

def test_read_one(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"complete": False, "title": "Learn to code", "description": "Need to learn", "id": 1, "priority": 5, "owner_id": 1}

def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not found"}

def test_create_todo(test_todo):
    request_data = {
        "title": "New todo",
        "description": "New todo description",
        "priority": 5,
        "complete": False,
    }

    response = client.post("/todos/todo", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.title=="New todo").first()
    assert model.priority == 5
    assert model.complete is False

def test_update_todo(test_todo):
    request_data = {
        "title": "Changed title",
        "description": "Need to learn",
        "priority": 5,
        "complete": False,
    }
    response = client.put("/todos/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.id == 1
    assert model.title == "Changed title"

def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "Changed title",
        "description": "Need to learn",
        "priority": 5,
        "complete": False,
    }
    response = client.put("/todos/todo/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not found"}

def test_delete_todo(test_todo):
    response = client.delete("/todos/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found(test_todo):
    response = client.delete("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not found"}
