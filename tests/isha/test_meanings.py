import pytest
from fastapi import status


@pytest.fixture
def sutra_data():
    return {"number": 10, "text": "Test Sutra text"}


@pytest.fixture
def meaning_data():
    return {"language": "en", "text": "Test meaning text"}


@pytest.mark.parametrize(
    "client_type",
    [
        "client",
        "authorized_client",
        "authorized_admin",
    ],
)
def test_get_meaning(
    client_type,
    client,
    authorized_client,
    authorized_admin,
    sutra_data,
    meaning_data,
):
    response = authorized_admin.post("/isha/sutras", json=sutra_data)
    assert response.status_code == status.HTTP_201_CREATED

    response = authorized_admin.post(
        f"/isha/sutras/{sutra_data.get("number")}/meaning",
        json=meaning_data,
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Map client_type to the corresponding client instance
    clients = {
        "client": client,
        "authorized_client": authorized_client,
        "authorized_admin": authorized_admin,
    }
    test_client = clients[client_type]

    response = test_client.get(
        f"/isha/sutras/{sutra_data.get("number")}/meaning?lang={meaning_data.get("language")}",
    )
    assert response.status_code == status.HTTP_200_OK

    meaning_data["id"] = 1
    assert response.json() == meaning_data


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
def test_add_meaning(
    client_type,
    expected_status,
    client,
    authorized_client,
    authorized_admin,
    sutra_data,
    meaning_data,
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

    response = test_client.post(
        f"/isha/sutras/{sutra_data.get("number")}/meaning",
        json=meaning_data,
    )
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
def test_update_meaning(
    client_type,
    expected_status,
    client,
    authorized_client,
    authorized_admin,
    sutra_data,
    meaning_data,
):

    response = authorized_admin.post("/isha/sutras", json=sutra_data)
    assert response.status_code == status.HTTP_201_CREATED

    response = authorized_admin.post(
        f"/isha/sutras/{sutra_data.get("number")}/meaning?lang={meaning_data.get("language")}",
        json=meaning_data,
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Map client_type to the corresponding client instance
    clients = {
        "client": client,
        "authorized_client": authorized_client,
        "authorized_admin": authorized_admin,
    }
    test_client = clients[client_type]

    updated_meaning = {
        "language": "en",
        "text": "Test meaning text",
    }

    response = test_client.put(
        f"/isha/sutras/{sutra_data.get("number")}/meaning?lang={meaning_data.get("language")}",
        json=updated_meaning,
    )
    assert response.status_code == expected_status

    if response.status_code == status.HTTP_204_NO_CONTENT:
        response = test_client.get(
            f"/isha/sutras/{sutra_data.get("number")}/meaning?lang={updated_meaning.get("language")}"
        )
        assert response.status_code == status.HTTP_200_OK
        updated_meaning["id"] = 1
        assert response.json() == updated_meaning


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
def test_delete_meaning(
    client_type,
    expected_status,
    client,
    authorized_client,
    authorized_admin,
    sutra_data,
    meaning_data,
):

    response = authorized_admin.post("/isha/sutras", json=sutra_data)
    assert response.status_code == status.HTTP_201_CREATED

    response = authorized_admin.post(
        f"/isha/sutras/{sutra_data.get("number")}/meaning?lang={meaning_data.get("language")}",
        json=meaning_data,
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Map client_type to the corresponding client instance
    clients = {
        "client": client,
        "authorized_client": authorized_client,
        "authorized_admin": authorized_admin,
    }
    test_client = clients[client_type]

    response = test_client.delete(
        f"/isha/sutras/{sutra_data.get("number")}/meaning?lang={meaning_data.get("language")}"
    )
    assert response.status_code == expected_status
