from pprint import pprint

import pytest
from fastapi import status


@pytest.fixture
def user_data():
    def _user_data(email: str):
        return {
            "email": email,
            "first_name": "FirstName",
            "last_name": "LastName",
            "password": "123",
            "phone_no": "9876543210",
        }

    return _user_data


def test_create_user(authorized_admin, user_data):
    response = authorized_admin.post(
        "/management/users",
        json=user_data(f"testuser@example.com"),
    )
    assert response.status_code == 201


def test_create_user_duplicate_email(authorized_admin, user_data):
    # First creation
    response = authorized_admin.post(
        "/management/users", json=user_data("duplicate@example.com")
    )
    assert response.status_code == 201

    # Attempt to create a duplicate
    response = authorized_admin.post(
        "/management/users", json=user_data("duplicate@example.com")
    )
    pprint(response.json())
    assert (
        response.status_code == status.HTTP_400_BAD_REQUEST
    )  # Expecting a 400 or similar error


def test_get_users(authorized_admin):
    response = authorized_admin.get("/management/users/")
    pprint(response.json())
    assert response.status_code == 200


def test_get_user_details(authorized_admin, test_user):
    user_id = test_user["id"]
    response = authorized_admin.get(f"/management/users/{user_id}")
    pprint(response.json())
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]


def test_get_user_details_unauthorized(client, test_user):
    user_id = test_user["id"]
    response = client.get(f"/management/users/{user_id}")
    assert (
        response.status_code == status.HTTP_401_UNAUTHORIZED
    )  # Expecting a 401 Unauthorized error


def test_admin_specific_access(authorized_client, user_data):
    # Attempt to create a user as a non-admin user
    response = authorized_client.post(
        "/management/users", json=user_data("unauthorized@example.com")
    )
    assert (
        response.status_code == status.HTTP_403_FORBIDDEN
    )  # Expecting a 403 Forbidden error


def test_user_password_change(client, test_user):
    # Log in and change password
    new_password_data = {
        "old_password": "123",
        "new_password": "newpassword123",
    }
    response = client.post("/management/users/change-password", json=new_password_data)
    assert response.status_code == 200

    # Log in with new password
    login_data = {"email": test_user["email"], "password": "newpassword123"}
    response = client.post("/login", json=login_data)
    assert response.status_code == 200
