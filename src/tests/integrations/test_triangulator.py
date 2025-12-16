import pytest
import struct
from unittest.mock import patch
from triangulator.server import create_app

@pytest.fixture
def client():
    app = create_app()
    return app.test_client()

def test_get_triangulation_valid_uuid(client):
    faux_pointset = struct.pack("<I", 0)
    create_response = client.post("/pointset", data=faux_pointset, content_type="application/octet-stream")
    assert create_response.status_code == 201
    pointset_data = create_response.get_json()
    pointset_id = pointset_data["pointSetId"]

    response = client.get(f"/triangulation/{pointset_id}")
    assert response.status_code == 200
    assert response.mimetype == "application/octet-stream"

def test_get_triangulation_invalid_uuid(client):
    response = client.get("/triangulation/invalid-uuid")
    assert response.status_code == 400
    data = response.get_json()
    assert data["code"] == "INVALID_UUID"
    assert "Format UUID invalide" in data["message"]

def test_get_triangulation_pointset_not_found(client):
    nonexistent_id = "12345678-1234-5678-9012-1234567890ab"
    response = client.get(f"/triangulation/{nonexistent_id}")
    assert response.status_code == 404
    data = response.get_json()
    assert data["code"] == "POINTSET_NOT_FOUND"

def test_get_triangulation_algorithm_failure(client):
    faux_pointset = struct.pack("<I", 0)
    create_response = client.post("/pointset", data=faux_pointset, content_type="application/octet-stream")
    assert create_response.status_code == 201
    pointset_data = create_response.get_json()
    pointset_id = pointset_data["pointSetId"]

    with patch("triangulator.routes.triangulation_routes.get_triangulation") as mock_get:
        mock_get.side_effect = RuntimeError("Échec de la triangulation: Algorithme non implémenté")

        response = client.get(f"/triangulation/{pointset_id}")
        assert response.status_code == 500
        data = response.get_json()
        if data:
            assert data["code"] == "TRIANGULATION_FAILED"

def test_get_triangulation_generic_error(client):
    with patch("triangulator.routes.triangulation_routes.get_triangulation") as mock_get:
        mock_get.side_effect = Exception("Erreur inattendue")

        response = client.get("/triangulation/12345678-1234-5678-9012-123456789012")
        assert response.status_code == 500
        data = response.get_json()
        if data: 
            assert data["code"] == "INTERNAL_ERROR"
            assert "Une erreur inattendue s'est produite" in data["message"]
