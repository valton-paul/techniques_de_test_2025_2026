import pytest
import struct
from unittest.mock import Mock

from triangulator.server import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as c:
        yield c

def test_get_pointset_valid(mocker, client):
    faux_pointset = struct.pack("<I", 2) + struct.pack("<ff", 1.0, 2.0) + struct.pack("<ff", 3.0, 4.0)

    mocker.patch("triangulator.routes.pointset_routes.get_pointset_by_id", return_value=(faux_pointset, 200))

    reponse = client.get("/pointset/1")

    assert reponse.status_code == 200
    assert reponse.data == faux_pointset

def test_get_pointset_invalid_uuid(mocker, client):
    mocker.patch("triangulator.routes.pointset_routes.get_pointset_by_id", 
                return_value=({"code": "INVALID_ID", "message": "Format d'ID invalide"}, 400))

    reponse = client.get("/pointset/invalid-uuid")

    assert reponse.status_code == 400

def test_get_pointset_not_found(mocker, client):
    mocker.patch("triangulator.routes.pointset_routes.get_pointset_by_id", 
                return_value=(b"", 404))

    reponse = client.get("/pointset/123e4567-e89b-12d3-a456-426614174999")

    assert reponse.status_code == 404

def test_create_pointset_valid(client):
    faux_pointset = struct.pack("<I", 2) + struct.pack("<ff", 1.0, 2.0) + struct.pack("<ff", 3.0, 4.0)

    reponse = client.post("/pointset", 
                         data=faux_pointset,
                         content_type="application/octet-stream")

    assert reponse.status_code == 201
    donnees = reponse.get_json()
    assert "pointSetId" in donnees

def test_create_pointset_no_data(client):
    reponse = client.post("/pointset", 
                         data="",
                         content_type="application/octet-stream")

    assert reponse.status_code == 400
    donnees = reponse.get_json()
    assert donnees["code"] == "INVALID_DATA"

def test_create_pointset_invalid_format(client):
    donnees_invalides = b"invalid binary data"

    reponse = client.post("/pointset", 
                         data=donnees_invalides,
                         content_type="application/octet-stream")

    assert reponse.status_code == 400
    donnees = reponse.get_json()
    assert donnees["code"] == "INVALID_FORMAT"
