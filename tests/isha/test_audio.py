import tempfile

import pytest
from fastapi import status
import os

# BASE_URL = "http://localhost:8100"
# UPANISHADS = "isha"
entity_suffix = "audio"

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
def audio_data():
    def _audio_data():
        return {"mode":"chant", "filepath": "static/isha/chant/sutra_0_A.mp3", }
    return _audio_data
def add_audio(upanishad: str = "test", chapter: int = 0, sutra_no: int = 10, mode: str = "chant", updateFilePath: str=""):
    # Determine the file suffix based on mode
    file_suffix = "A" if mode == "chant" else "B"
    # Construct the file path
    if updateFilePath == "":
        if upanishad == 'isha': file_path = f"audio/{upanishad}/{sutra_no}_{file_suffix}.mp3"
        else: file_path = f"audio/{upanishad}/{chapter}/{sutra_no}_{file_suffix}.mp3"
    else: file_path = updateFilePath
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Audio file not found: {file_path}")
        return None  # Return None if the file doesn't exist
    # Prepare the files for multipart/form-data
    files = {"file": ("audio.mp3", open(file_path, "rb"), "audio/mpeg")}
    return files

@pytest.mark.parametrize("client_type",["client", "authorized_client","authorized_admin",],)
def test_get_audio(client_type, client, authorized_client, authorized_admin, project_data, sutra_data, audio_data,):
    response = authorized_admin.post("/projects/?name=test&description=testdesc", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post("/isha/sutras/", json=sutra_data())
    assert response.status_code == status.HTTP_201_CREATED

    # Create a temporary directory and mp3 file
    with tempfile.TemporaryDirectory() as temp_dir:
        file_name = "test_audio.mp3"
        file_path = os.path.join(temp_dir, file_name)
        # Create an empty file
        with open(file_path, "wb") as f: pass # create an empty file.
        files = add_audio(sutra_data()["project"]["name"], sutra_data()["sutra"]["chapter"], sutra_data()["sutra"]["number"], audio_data()["mode"], file_path)
        if files is None: pytest.skip("Audio file not found, skipping test.")
        data = {"mode": audio_data()["mode"], "filepath": audio_data()["filepath"]}
        response = authorized_admin.post(
            f"/isha/sutras/{sutra_data()['project']['name']}/{sutra_data()['sutra']['chapter']}/{sutra_data()['sutra']['number']}/{entity_suffix}?mode={audio_data()["mode"]}",
            files=files,
            data=data,
        )
        assert response.status_code == status.HTTP_201_CREATED
        # Map client_type to the corresponding client instance
        clients = {"client": client, "authorized_client": authorized_client, "authorized_admin": authorized_admin,}
        test_client = clients[client_type]
        response = test_client.get(f"/isha/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}?mode={audio_data()["mode"]}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"file_path": f"static/isha/{audio_data()["mode"]}/sutra_{sutra_data()["sutra"]["number"]}.mp3"}
@pytest.mark.parametrize("client_type, expected_status",
    [
        ("client", status.HTTP_401_UNAUTHORIZED,),  # Unauthorized client should return 401
        ("authorized_client", status.HTTP_201_CREATED,),  # Authorized regular user should return 201
        ("authorized_admin", status.HTTP_201_CREATED,),  # Authorized admin should also return 201
    ],
)
def test_add_audio(client_type, expected_status, client, authorized_client, authorized_admin, project_data, sutra_data, audio_data):
    response = authorized_admin.post("/projects/?name=test&description=testdesc", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post("/isha/sutras/", json=sutra_data())
    assert response.status_code == status.HTTP_201_CREATED
    # Map client_type to the corresponding client instance
    clients = {"client": client, "authorized_client": authorized_client, "authorized_admin": authorized_admin}
    test_client = clients[client_type]

    # Create a temporary directory and mp3 file
    with tempfile.TemporaryDirectory() as temp_dir:
        file_name = "test_audio.mp3"
        file_path = os.path.join(temp_dir, file_name)

        # Create an empty file
        with open(file_path, "wb") as f:
            pass # create an empty file.
        files = add_audio(sutra_data()["project"]["name"], sutra_data()["sutra"]["chapter"], sutra_data()["sutra"]["number"], audio_data()["mode"], file_path)
        if files is None: pytest.skip("Audio file not found, skipping test.")
        data = {"mode": audio_data()["mode"], "filepath": audio_data()["filepath"]}
        response = test_client.post(
            f"/isha/sutras/{sutra_data()['project']['name']}/{sutra_data()['sutra']['chapter']}/{sutra_data()['sutra']['number']}/{entity_suffix}?mode={audio_data()["mode"]}",
            files=files,
            data=data,
        )
        # print(f"Response Content:{response.content}")
        assert response.status_code == expected_status
@pytest.mark.parametrize("client_type, expected_status",
    [
        ("client", status.HTTP_401_UNAUTHORIZED,),  # Unauthorized client should return 401
        ("authorized_client", status.HTTP_204_NO_CONTENT,),  # Authorized regular user should return 201
        ("authorized_admin", status.HTTP_204_NO_CONTENT,),  # Authorized admin should also return 201
    ],
)
def test_update_audio(client_type, expected_status, client, authorized_client, authorized_admin, project_data, sutra_data, audio_data,):
    response = authorized_admin.post("/projects/?name=test&description=testdesc", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post("/isha/sutras/", json=sutra_data())
    assert response.status_code == status.HTTP_201_CREATED
    # Create a temporary directory and mp3 file
    with tempfile.TemporaryDirectory() as temp_dir:
        file_name = "test_audio.mp3"
        file_path = os.path.join(temp_dir, file_name)
        # Create an empty file
        with open(file_path, "wb") as f: pass # create an empty file.
        files = add_audio(sutra_data()["project"]["name"], sutra_data()["sutra"]["chapter"], sutra_data()["sutra"]["number"], audio_data()["mode"], file_path)
        if files is None: pytest.skip("Audio file not found, skipping test.")
        data = {"mode": audio_data()["mode"], "filepath": audio_data()["filepath"]}
        response = authorized_admin.post(
            f"/isha/sutras/{sutra_data()['project']['name']}/{sutra_data()['sutra']['chapter']}/{sutra_data()['sutra']['number']}/{entity_suffix}?mode={audio_data()["mode"]}",
            files=files,
            data=data,
        )
        assert response.status_code == status.HTTP_201_CREATED

        # Map client_type to the corresponding client instance
        clients = {"client": client, "authorized_client": authorized_client, "authorized_admin": authorized_admin,}
        test_client = clients[client_type]
        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = "test_audio_updated.mp3"
            file_path = os.path.join(temp_dir, file_name)
            # Create an empty file
            with open(file_path, "wb") as f: pass  # create an empty file.
            files = add_audio(sutra_data()["project"]["name"], sutra_data()["sutra"]["chapter"],
                              sutra_data()["sutra"]["number"], audio_data()["mode"], file_path)
            if files is None: pytest.skip("Audio file not found, skipping test.")
            data = {"mode": audio_data()["mode"], "filepath": audio_data()["filepath"]}
            response = test_client.put(
                f"/isha/sutras/{sutra_data()['project']['name']}/{sutra_data()['sutra']['chapter']}/{sutra_data()['sutra']['number']}/{entity_suffix}?mode={audio_data()["mode"]}",
                files=files,
                data=data,
            )
            # print(f"response {response.content}")
            assert response.status_code == expected_status
            if response.status_code == status.HTTP_202_ACCEPTED:
                response = test_client.get(f"/isha/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}?lang={audio_data()["filepath"]}&phil={audio_data()["mode"]}",)
                assert response.status_code == status.HTTP_200_OK
                assert response.json() == {"file_path": f"static/isha/{audio_data()["mode"]}/sutra_{sutra_data()["sutra"]["number"]}.mp3"}
@pytest.mark.parametrize("client_type, expected_status",
    [
        ("client", status.HTTP_401_UNAUTHORIZED,),  # Unauthorized client should return 401
        ("authorized_client", status.HTTP_403_FORBIDDEN,),  # Authorized regular user should return 403
        ("authorized_admin", status.HTTP_204_NO_CONTENT,),  # Authorized admin should also return 201
    ],
)
def test_delete_audio(client_type, expected_status, client, authorized_client, authorized_admin, project_data, sutra_data, audio_data,):
    response = authorized_admin.post("/projects/?name=test&description=testdesc", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.post("/isha/sutras/", json=sutra_data())
    assert response.status_code == status.HTTP_201_CREATED
    # Create a temporary directory and mp3 file
    with tempfile.TemporaryDirectory() as temp_dir:
        file_name = "test_audio.mp3"
        file_path = os.path.join(temp_dir, file_name)
        # Create an empty file
        with open(file_path, "wb") as f: pass  # create an empty file.
        files = add_audio(sutra_data()["project"]["name"], sutra_data()["sutra"]["chapter"],
                          sutra_data()["sutra"]["number"], audio_data()["mode"], file_path)
        if files is None: pytest.skip("Audio file not found, skipping test.")
        data = {"mode": audio_data()["mode"], "filepath": audio_data()["filepath"]}
        response = authorized_admin.post(
            f"/isha/sutras/{sutra_data()['project']['name']}/{sutra_data()['sutra']['chapter']}/{sutra_data()['sutra']['number']}/{entity_suffix}?mode={audio_data()["mode"]}",
            files=files,
            data=data,
        )
        assert response.status_code == status.HTTP_201_CREATED

        # Map client_type to the corresponding client instance
        clients = {"client": client, "authorized_client": authorized_client, "authorized_admin": authorized_admin,}
        test_client = clients[client_type]
        response = test_client.delete(f"/isha/sutras/{sutra_data()["project"]["name"]}/{sutra_data()["sutra"]["chapter"]}/{sutra_data()["sutra"]["number"]}/{entity_suffix}?mode={audio_data()["mode"]}")
        assert response.status_code == expected_status
