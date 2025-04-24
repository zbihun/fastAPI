import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

from database import Base
from main import app
from models import Todos, Users
from routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:dolyna@localhost/TESTToDoAppDB"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:

        yield db

    finally:
        db.close()


def override_get_current_user():
    return {"username": "test", "id": 1, "user_role": "admin"}


client = TestClient(app)


@pytest.fixture
def test_todo():
    db = TestingSessionLocal()
    user_item = Users(
        id=1,
        email="test",
        username="test",
        first_name="test",
        last_name="test",
        hashed_password=bcrypt_context.hash("test"),
        is_active=True,
        role="test",
        phone_number="0123456789",
    )
    db.add(user_item)
    db.commit()

    todo_item = Todos(
        id=1,
        title="Learn to code",
        description="Need to learn",
        priority=5,
        complete=False,
        owner_id=1
    )
    db.add(todo_item)
    db.commit()
    yield todo_item
    with engine.connect() as connection:
        connection.execute(text("DELETE from todos;"))
        connection.execute(text("DELETE from users;"))
        connection.commit()

@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    user_item = Users(
        id=1,
        email="test",
        username="test",
        first_name="test",
        last_name="test",
        hashed_password=bcrypt_context.hash("test"),
        is_active=True,
        role="admin",
        phone_number="0123456789",
    )
    db.add(user_item)
    db.commit()

    yield user_item
    with engine.connect() as connection:
        connection.execute(text("DELETE from users;"))
        connection.commit()
