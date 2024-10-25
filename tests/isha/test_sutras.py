import pytest


@pytest.fixture
def sutra_data():
    def _sutra_data():
        return {"number": 1, "text": ""}

    return _sutra_data


@pytest.mark.parametrize(
    "client_type, expected_status",
    [
        ("client", 200),  # Unauthorized client should return 200
        ("authorized_client", 200),  # Authorized regular user should return 200
        ("authorized_admin", 200),  # Authorized admin should also return 200
    ],
)
def test_get_sutra(
    client_type, expected_status, client, authorized_client, authorized_admin
):

    authorized_admin.post("/")

    # Map client_type to the corresponding client instance
    clients = {
        "client": client,
        "authorized_client": authorized_client,
        "authorized_admin": authorized_admin,
    }
    # Get the client instance based on the parameter
    test_client = clients[client_type]

    # Make the GET request
    response = test_client.get("/sutra")

    # Check if the status code matches the expected status for this client type
    assert response.status_code == expected_status
    #
    # # Add additional assertions as needed, e.g., checking content for authorized users
    # if expected_status == 200:
    #     assert (
    #         "expected_content" in response.json()
    #     )  # Replace "expected_content" with actual expected content
