import pytest
from fastapi import status


@pytest.fixture
def sutra_data():
    return {"number": 10, "text": "Test Sutra text"}


@pytest.mark.parametrize(
    "client_type",
    [
        "client",
        "authorized_client",
        "authorized_admin",
    ],
)
def test_get_sutra(
    client_type,
    client,
    authorized_client,
    authorized_admin,
    sutra_data,
):
    response = authorized_admin.post("/isha/sutras", json=sutra_data)
    assert response.status_code == status.HTTP_201_CREATED

    # Map client_type to the corresponding client instance
    clients = {
        "client": client,
        "authorized_client": authorized_client,
        "authorized_admin": authorized_admin,
    }
    test_client = clients[client_type]

    response = test_client.get("/isha/sutras")
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0] == {"id": 1, "number": sutra_data.get("number")}


@pytest.mark.parametrize(
    "client_type, expected_status",
    [
        (
            "client",
            status.HTTP_401_UNAUTHORIZED,
        ),  # Unauthorized client should return 401
        (
            "authorized_client",
            status.HTTP_201_CREATED,
        ),  # Authorized regular user should return 201
        (
            "authorized_admin",
            status.HTTP_201_CREATED,
        ),  # Authorized admin should also return 201
    ],
)
def test_add_sutra(
    client_type,
    expected_status,
    client,
    authorized_client,
    authorized_admin,
    sutra_data,
):

    # Map client_type to the corresponding client instance
    clients = {
        "client": client,
        "authorized_client": authorized_client,
        "authorized_admin": authorized_admin,
    }
    test_client = clients[client_type]

    response = test_client.post("/isha/sutras", json=sutra_data)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "client_type, expected_status",
    [
        (
            "client",
            status.HTTP_401_UNAUTHORIZED,
        ),  # Unauthorized client should return 401
        (
            "authorized_client",
            status.HTTP_204_NO_CONTENT,
        ),  # Authorized regular user should return 201
        (
            "authorized_admin",
            status.HTTP_204_NO_CONTENT,
        ),  # Authorized admin should also return 201
    ],
)
def test_update_sutra(
    client_type,
    expected_status,
    client,
    authorized_client,
    authorized_admin,
    sutra_data,
):

    response = authorized_admin.post("/isha/sutras", json=sutra_data)
    assert response.status_code == status.HTTP_201_CREATED

    # Map client_type to the corresponding client instance
    clients = {
        "client": client,
        "authorized_client": authorized_client,
        "authorized_admin": authorized_admin,
    }
    test_client = clients[client_type]

    updated_sutra = {"id": 1, "number": 10, "text": "Updated sutra message"}

    response = test_client.put(
        f"/isha/sutras/{sutra_data.get("number")}", json=updated_sutra
    )
    assert response.status_code == expected_status

    if response.status_code == status.HTTP_204_NO_CONTENT:
        response = test_client.get(f"/isha/sutras/{sutra_data.get("number")}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == updated_sutra


@pytest.mark.parametrize(
    "client_type, expected_status",
    [
        (
            "client",
            status.HTTP_401_UNAUTHORIZED,
        ),  # Unauthorized client should return 401
        (
            "authorized_client",
            status.HTTP_403_FORBIDDEN,
        ),  # Authorized regular user should return 201
        (
            "authorized_admin",
            status.HTTP_204_NO_CONTENT,
        ),  # Authorized admin should also return 201
    ],
)
def test_delete_sutra(
    client_type,
    expected_status,
    client,
    authorized_client,
    authorized_admin,
    sutra_data,
):

    response = authorized_admin.post("/isha/sutras", json=sutra_data)
    assert response.status_code == status.HTTP_201_CREATED

    # Map client_type to the corresponding client instance
    clients = {
        "client": client,
        "authorized_client": authorized_client,
        "authorized_admin": authorized_admin,
    }
    test_client = clients[client_type]

    response = test_client.delete(f"/isha/sutras/{sutra_data.get("number")}")
    assert response.status_code == expected_status
