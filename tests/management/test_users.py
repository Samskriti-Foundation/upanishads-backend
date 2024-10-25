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
        "/users",
        json=user_data(f"testuser@example.com"),
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_user_duplicate_email(authorized_admin, user_data):
    # First creation
    response = authorized_admin.post("/users", json=user_data("duplicate@example.com"))
    assert response.status_code == status.HTTP_201_CREATED

    # Attempt to create a duplicate
    response = authorized_admin.post("/users", json=user_data("duplicate@example.com"))
    assert response.status_code == status.HTTP_409_CONFLICT


def test_get_users(authorized_admin):
    response = authorized_admin.get("/users/")
    assert response.status_code == status.HTTP_200_OK


def test_get_user_details(authorized_admin, user_data):

    response = authorized_admin.post("/users", json=user_data("duplicate@example.com"))
    assert response.status_code == status.HTTP_201_CREATED

    user_id = response.json()["id"]

    response = authorized_admin.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK


def test_get_user_details_unauthorized(
    authorized_admin, authorized_client, client, user_data
):
    response = authorized_admin.post("/users", json=user_data("duplicate@example.com"))
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_client.get(f"/users/")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get(f"/users/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_admin_specific_access(authorized_client, user_data):
    # Attempt to create a user as a non-admin user
    response = authorized_client.post(
        "/users", json=user_data("unauthorized@example.com")
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


# def test_user_password_change(client, test_user):
#     # Log in and change password
#     new_password_data = {
#         "old_password": "123",
#         "new_password": "newpassword123",
#     }
#     response = client.post("/users/change-password", json=new_password_data)
#     assert response.status_code == status.HTTP_200_OK
#
#     # Log in with new password
#     login_data = {"email": test_user["email"], "password": "newpassword123"}
#     response = client.post("/login", json=login_data)
#     assert response.status_code == status.HTTP_200_OK
