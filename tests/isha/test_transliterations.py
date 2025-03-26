import pytest
from fastapi import status

entity_suffix = "transliteration"

@pytest.fixture
def sutra_data():
    def _sutra_data():
        return {"sutra": {"id":0, "chapter": 0, "number": 10, "text": "Test Sutra text", "project_id": 1}, "project":{"name":"test"}}
    return _sutra_data
@pytest.fixture
def project_data():
    def _project_data():
        return {"name": 'test', "description": "testopanishad"}
    return _project_data
@pytest.fixture
def transliteration_data():
    def _transliteration_data():
        return {"language": "en", "text": "Test transliteration text"}
    return _transliteration_data

@pytest.mark.parametrize("client_type",["client", "authorized_client","authorized_admin",],)
def test_get_transliteration(client_type, client, authorized_client, authorized_admin, project_data, sutra_data, transliteration_data,):
    response = authorized_admin.post("/projects/?name=test&description=testdesc", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post("/isha/sutras/", json=sutra_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post(f"/isha/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}", json=transliteration_data())
    assert response.status_code == status.HTTP_201_CREATED
    # Map client_type to the corresponding client instance
    clients = {"client": client, "authorized_client": authorized_client, "authorized_admin": authorized_admin,}
    test_client = clients[client_type]
    response = test_client.get(f"/isha/sutras/test/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}?lang={transliteration_data()["language"]}",)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "text": transliteration_data()["text"], "language": transliteration_data()["language"]}
@pytest.mark.parametrize("client_type, expected_status",
    [
        ("client", status.HTTP_401_UNAUTHORIZED,),  # Unauthorized client should return 401
        ("authorized_client", status.HTTP_201_CREATED,),  # Authorized regular user should return 201
        ("authorized_admin", status.HTTP_201_CREATED,),  # Authorized admin should also return 201
    ],
)
def test_add_transliteration(client_type, expected_status, client, authorized_client, authorized_admin, project_data, sutra_data, transliteration_data,):
    response = authorized_admin.post("/projects/?name=test&description=testdesc", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post("/isha/sutras/", json=sutra_data())
    assert response.status_code == status.HTTP_201_CREATED

    # Map client_type to the corresponding client instance
    clients = {"client": client, "authorized_client": authorized_client, "authorized_admin": authorized_admin,}
    test_client = clients[client_type]
    response = test_client.post(f"/isha/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}", json=transliteration_data())
    assert response.status_code == expected_status
@pytest.mark.parametrize("client_type, expected_status",
    [
        ("client", status.HTTP_401_UNAUTHORIZED,),  # Unauthorized client should return 401
        ("authorized_client", status.HTTP_202_ACCEPTED,),  # Authorized regular user should return 201
        ("authorized_admin", status.HTTP_202_ACCEPTED,),  # Authorized admin should also return 201
    ],
)
def test_update_transliteration(client_type, expected_status, client, authorized_client, authorized_admin, project_data, sutra_data, transliteration_data,):
    response = authorized_admin.post("/projects/?name=test&description=testdesc", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post("/isha/sutras/", json=sutra_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post(f"/isha/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}", json=transliteration_data())
    assert response.status_code == status.HTTP_201_CREATED
    # Map client_type to the corresponding client instance
    clients = {"client": client, "authorized_client": authorized_client, "authorized_admin": authorized_admin,}
    test_client = clients[client_type]
    updated_transliteration = {"id":1, "language": "en","text": "Test transliteration text",}
    response = test_client.put(f"/isha/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}?lang={updated_transliteration["language"]}", json=updated_transliteration)
    assert response.status_code == expected_status
    if response.status_code == status.HTTP_202_ACCEPTED:
        response = test_client.get(f"/isha/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}?lang={transliteration_data()["language"]}",)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == updated_transliteration
@pytest.mark.parametrize("client_type, expected_status",
    [
        ("client", status.HTTP_401_UNAUTHORIZED,),  # Unauthorized client should return 401
        ("authorized_client", status.HTTP_403_FORBIDDEN,),  # Authorized regular user should return 201
        ("authorized_admin", status.HTTP_200_OK,),  # Authorized admin should also return 201
    ],
)
def test_delete_transliteration(client_type, expected_status, client, authorized_client, authorized_admin, project_data, sutra_data, transliteration_data,):
    response = authorized_admin.post("/projects/?name=test&description=testdesc", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post("/isha/sutras/", json=sutra_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post(f"/isha/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}", json=transliteration_data())
    assert response.status_code == status.HTTP_201_CREATED
# Map client_type to the corresponding client instance
    clients = {"client": client, "authorized_client": authorized_client, "authorized_admin": authorized_admin,}
    test_client = clients[client_type]
    response = test_client.delete(f"/isha/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}?lang={transliteration_data()["language"]}")
    assert response.status_code == expected_status
