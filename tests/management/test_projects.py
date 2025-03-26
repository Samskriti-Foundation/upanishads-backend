import re

import pytest
from fastapi import status

@pytest.fixture
def project_data():
    def _project_data():
        return {"name": 'test', "description": "testopanishad"}
    return _project_data

def test_create_project(authorized_admin, project_data):
    response = authorized_admin.post("/projects/?name=test&description=testdesc", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED

def test_get_project(authorized_admin, project_data):
    response = authorized_admin.post("/projects/?name=test&description=testdesc", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    response = authorized_admin.get('/projects_by_name/test')
    assert response.status_code == 200

def test_create_project_duplicate(authorized_admin, project_data):
    # First creation
    response = authorized_admin.post("/projects?name=test&description=testdesc", json=project_data())
    assert response.status_code == status.HTTP_201_CREATED
    # Attempt to create a duplicate
    response = authorized_admin.post("/projects?name=test&description=testdescript", json=project_data())
    assert response.status_code == status.HTTP_409_CONFLICT

def test_get_projects(authorized_admin):
    response = authorized_admin.get("/projects/")
    assert response.status_code == status.HTTP_200_OK
