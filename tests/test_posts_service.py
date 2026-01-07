from re import M
from unittest import mock
from fastapi import Request
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.dependencies import get_db
from core.main import app
from database.connection import Base
import os
from dotenv import load_dotenv
from core.base_routing import main_router as router

load_dotenv()


# create a test db
engine = create_engine(os.getenv('TEST_DATABASE_URL', ''), pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# fixture for mock db session
@pytest.fixture()
def mock_db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session =  TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

# fixture for db migrations
@pytest.fixture(scope="session", autouse=True)
def db():
    # add all tables and delete all after tests
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class MockUser:
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    community_instance_id = "123e4567-e89b-12d3-a233-426614174000"


async def mock_request_with_user(request: Request, call_next):
    request.state.user = MockUser()
    response = await call_next(request)
    return response


# mock a client
@pytest.fixture()
def client_app(mock_db_session):

    app.middleware("http")(mock_request_with_user)

    def override_get_db():
        yield mock_db_session
    # to override the get_db dependency
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client: 
        yield client
        

# background task to test
@pytest.fixture()
def mock_background_task(monkeypatch):
    monkeypatch.setattr(
        "posts.service.index_documents",
        lambda *args, **kwargs: None
    )

# mock authorization using the user mock

def test_create_post_success(request: Request, client_app: TestClient, mock_db_session) -> None:

    post_data = {
        "title": "Test Event",
        "description": "This is a test event",
        "post_type": "event",
        "user_id": MockUser.user_id,
        "community_instance_id": MockUser.community_instance_id,
        "pin_location": "Test Location",
    }
    response = client_app.post("api/v1/posts/create", json=post_data)
    assert response.status_code == 200
    assert response.json().get("message") == "Post created successfully"
    




