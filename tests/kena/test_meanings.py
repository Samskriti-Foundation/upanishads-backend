import pytest
from fastapi import status

entity_suffix = "meaning"

@pytest.fixture
def sutra_data():
    def _sutra_data():
        return {"sutra": {"id":0, "chapter": 0, "number": 10, "text": "Test Sutra text", "project_id": 1}, "project":{"name":"kena_test"}}
    return _sutra_data
@pytest.fixture
def project_data():
    def _project_data():
        return {"name": 'kena_test', "description": "testopanishad"}
    return _project_data
@pytest.fixture
def meaning_data():
    def _meaning_data():
        return {"language": "en", "text": "Test meaning text"}
    return _meaning_data

@pytest.mark.parametrize("client_type",["client", "authorized_client","authorized_admin",],)
def test_get_meaning(client_type, client, authorized_client, authorized_admin, project_data, sutra_data, meaning_data,):
    response = authorized_admin.post("/projects/?name=kena_test&description=testdesc", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post("/kena/sutras/", json=sutra_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post(f"/kena/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}", json=meaning_data())
    assert response.status_code == status.HTTP_201_CREATED
    # Map client_type to the corresponding client instance
    clients = {"client": client, "authorized_client": authorized_client, "authorized_admin": authorized_admin,}
    test_client = clients[client_type]
    response = test_client.get(f"/kena/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}?lang={meaning_data()["language"]}",)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "text": meaning_data()["text"], "language": meaning_data()["language"]}
@pytest.mark.parametrize("client_type, expected_status",
    [
        ("client", status.HTTP_401_UNAUTHORIZED,),  # Unauthorized client should return 401
        ("authorized_client", status.HTTP_201_CREATED,),  # Authorized regular user should return 201
        ("authorized_admin", status.HTTP_201_CREATED,),  # Authorized admin should also return 201
    ],
)
def test_add_meaning(client_type, expected_status, client, authorized_client, authorized_admin, project_data, sutra_data, meaning_data,):
    response = authorized_admin.post("/projects/?name=kena_test&description=testdesc", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post("/kena/sutras/", json=sutra_data())
    assert response.status_code == status.HTTP_201_CREATED

    # Map client_type to the corresponding client instance
    clients = {"client": client, "authorized_client": authorized_client, "authorized_admin": authorized_admin,}
    test_client = clients[client_type]
    response = test_client.post(f"/kena/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}", json=meaning_data())
    assert response.status_code == expected_status
@pytest.mark.parametrize("client_type, expected_status",
    [
        ("client", status.HTTP_401_UNAUTHORIZED,),  # Unauthorized client should return 401
        ("authorized_client", status.HTTP_202_ACCEPTED,),  # Authorized regular user should return 201
        ("authorized_admin", status.HTTP_202_ACCEPTED,),  # Authorized admin should also return 201
    ],
)
def test_update_meaning(client_type, expected_status, client, authorized_client, authorized_admin, project_data, sutra_data, meaning_data,):
    response = authorized_admin.post("/projects/?name=kena_test&description=testdesc", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post("/kena/sutras/", json=sutra_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post(f"/kena/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}", json=meaning_data())
    assert response.status_code == status.HTTP_201_CREATED
    # Map client_type to the corresponding client instance
    clients = {"client": client, "authorized_client": authorized_client, "authorized_admin": authorized_admin,}
    test_client = clients[client_type]
    updated_meaning = {"id":1, "language": "en","text": "Test meaning text",}
    response = test_client.put(f"/kena/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}?lang={updated_meaning["language"]}", json=updated_meaning)
    assert response.status_code == expected_status
    if response.status_code == status.HTTP_202_ACCEPTED:
        response = test_client.get(f"/kena/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}?lang={meaning_data()["language"]}",)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == updated_meaning
@pytest.mark.parametrize("client_type, expected_status",
    [
        ("client", status.HTTP_401_UNAUTHORIZED,),  # Unauthorized client should return 401
        ("authorized_client", status.HTTP_403_FORBIDDEN,),  # Authorized regular user should return 201
        ("authorized_admin", status.HTTP_200_OK,),  # Authorized admin should also return 201
    ],
)
def test_delete_meaning(client_type, expected_status, client, authorized_client, authorized_admin, project_data, sutra_data, meaning_data,):
    response = authorized_admin.post("/projects/?name=kena_test&description=testdesc", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post("/kena/sutras/", json=sutra_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post(f"/kena/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}", json=meaning_data())
    assert response.status_code == status.HTTP_201_CREATED
# Map client_type to the corresponding client instance
    clients = {"client": client, "authorized_client": authorized_client, "authorized_admin": authorized_admin,}
    test_client = clients[client_type]
    response = test_client.delete(f"/kena/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}?lang={meaning_data()["language"]}")
    assert response.status_code == expected_status
