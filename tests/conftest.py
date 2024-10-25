import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import utils
from app.config import settings
from app.database import Base, get_db
from app.isha.main import isha
from app.main import app
from app.models import User
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = settings.test_db_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    isha.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def test_admin(session):
    user_data = {
        "first_name": "Admin",
        "last_name": "Admin",
        "email": "admin@example.com",
        "password": "123",
        "is_admin": True,
    }

    hashed_password = utils.hash_password(user_data["password"])
    user_data["password"] = hashed_password
    new_user = User(**user_data)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    assert new_user.email == user_data["email"]
    assert new_user.first_name == user_data["first_name"]
    assert new_user.last_name == user_data["last_name"]
    assert new_user.is_admin == user_data["is_admin"]

    return new_user


@pytest.fixture
def token_admin(test_admin):
    test_admin = test_admin.__dict__
    return create_access_token(
        {"user_id": test_admin["id"], "is_admin": test_admin["is_admin"]}
    )


class AuthorizedClient:
    def __init__(self, client, token):
        self.client = client
        self.token = token

    def _get_headers(self, headers):
        return {**headers, "Authorization": f"Bearer {self.token}"}

    def get(self, url, **kwargs):
        headers = self._get_headers(kwargs.pop("headers", {}))
        return self.client.get(url, headers=headers, **kwargs)

    def post(self, url, **kwargs):
        headers = self._get_headers(kwargs.pop("headers", {}))
        return self.client.post(url, headers=headers, **kwargs)

    def put(self, url, **kwargs):
        headers = self._get_headers(kwargs.pop("headers", {}))
        return self.client.put(url, headers=headers, **kwargs)

    def delete(self, url, **kwargs):
        headers = self._get_headers(kwargs.pop("headers", {}))
        return self.client.delete(url, headers=headers, **kwargs)


@pytest.fixture
def authorized_admin(client, token_admin):
    return AuthorizedClient(client, token_admin)


@pytest.fixture
def test_user(authorized_admin):
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "test@example.com",
        "password": "123",
    }

    res = authorized_admin.post("/users/", json=user_data)

    assert res.status_code == status.HTTP_201_CREATED

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"], "is_admin": "false"})


@pytest.fixture
def authorized_client(client, token):
    return AuthorizedClient(client, token)
