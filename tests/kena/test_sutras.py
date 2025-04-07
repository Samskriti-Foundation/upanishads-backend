import pytest
from fastapi import status


@pytest.fixture
def sutra_data():
    def _sutra_data():
        return {"sutra": {"id":0, "chapter": 0, "number": 10, "text": "Test Sutra text", "project_id": 1}, "project":{"name":"kena_test", "description": "kena test description"}}
    return _sutra_data
@pytest.fixture
def project_data():
    def _project_data():
        return {"name": 'kena_test', "description": "kena_testopanishad"}
    return _project_data

@pytest.mark.parametrize("client_type",["client", "authorized_client", "authorized_admin"])
def test_get_sutra(client_type, client, authorized_client, authorized_admin, sutra_data, project_data):
    response = authorized_admin.post(f"/projects/?name={sutra_data()['project']['name']}&description={sutra_data()['project']['description']}", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post("/kena/sutras/", json=sutra_data())
    assert response.status_code == status.HTTP_201_CREATED

    # Map client_type to the corresponding client instance
    clients = {"client": client, "authorized_client": authorized_client, "authorized_admin": authorized_admin}
    test_client = clients[client_type]

    response = test_client.get(f"/kena/sutras/{sutra_data()["project"]["name"]}/0/10")
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert len(response_data) == 4
    assert response_data == {"id": 1, "chapter": sutra_data()["sutra"]["chapter"], "number": sutra_data()["sutra"]["number"], "text": sutra_data()["sutra"]["text"]}

@pytest.mark.parametrize("client_type, expected_status",
    [
        ("client", status.HTTP_401_UNAUTHORIZED,),  # Unauthorized client should return 401
        ("authorized_client", status.HTTP_201_CREATED,),  # Authorized regular user should return 201
        ("authorized_admin", status.HTTP_201_CREATED,)  # Authorized admin should also return 201
    ],
)
def test_add_sutra(
    client_type,
    expected_status,
    client,
    authorized_client,
    authorized_admin,
    sutra_data,
    project_data
):

    # Map client_type to the corresponding client instance
    clients = {
        "client": client,
        "authorized_client": authorized_client,
        "authorized_admin": authorized_admin,
    }
    test_client = clients[client_type]

    response = test_client.post(f"/projects/?name={sutra_data()['project']['name']}&description={sutra_data()['project']['description']}", json=project_data())
    assert response.status_code == expected_status
    response = test_client.post("/kena/sutras", json=sutra_data())
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
            status.HTTP_202_ACCEPTED,
        ),  # Authorized regular user should return 201
        (
            "authorized_admin",
            status.HTTP_202_ACCEPTED,
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
    project_data
):
    response = authorized_admin.post(f"/projects/?name={sutra_data()['project']['name']}&description={sutra_data()['project']['description']}", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post("/kena/sutras/", json=sutra_data())
    assert response.status_code == status.HTTP_201_CREATED

    # Map client_type to the corresponding client instance
    clients = {
        "client": client,
        "authorized_client": authorized_client,
        "authorized_admin": authorized_admin,
    }
    test_client = clients[client_type]

    updated_sutra = {"id": 1, "chapter": 0, "number": 10, "text": "Updated sutra message"}
    sutra_data = sutra_data()
    response = test_client.put(f"/kena/sutras/{sutra_data["project"]["name"]}/{sutra_data["sutra"]["chapter"]}/{sutra_data["sutra"]["number"]}", json=updated_sutra)
    assert response.status_code == expected_status

    if response.status_code == status.HTTP_202_ACCEPTED:
        response = test_client.get(f"/kena/sutras/{sutra_data["project"]["name"]}/{sutra_data["sutra"]["chapter"]}/{sutra_data["sutra"]["number"]}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == updated_sutra

@pytest.mark.parametrize(
    "client_type, expected_status",
    [
        ("client", status.HTTP_401_UNAUTHORIZED,),  # Unauthorized client should return 401
        ("authorized_client", status.HTTP_403_FORBIDDEN,),  # Authorized regular user should return 201
        ("authorized_admin", status.HTTP_200_OK,),  # Authorized admin should also return 201
    ],
)
def test_delete_sutra(
    client_type,
    expected_status,
    client,
    authorized_client,
    authorized_admin,
    sutra_data,
    project_data
):
    response = authorized_admin.post(f"/projects/?name={sutra_data()['project']['name']}&description={sutra_data()['project']['description']}", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post("/kena/sutras/", json=sutra_data())
    assert response.status_code == status.HTTP_201_CREATED
    # Map client_type to the corresponding client instance
    clients = {
        "client": client,
        "authorized_client": authorized_client,
        "authorized_admin": authorized_admin,
    }
    test_client = clients[client_type]
    sutra_data = sutra_data()
    # print(f"sutra data: {sutra_data["project"]["name"]}/{sutra_data["sutra"]["chapter"]}/{sutra_data["sutra"]["number"]}")
    response = test_client.delete(f"/kena/sutras/{sutra_data["project"]["name"]}/{sutra_data["sutra"]["chapter"]}/{sutra_data["sutra"]["number"]}")
    assert response.status_code == expected_status
