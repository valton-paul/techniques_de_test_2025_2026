import importlib
import uuid
from flask import Blueprint, Response, request, jsonify
from typing import Dict

pointset_routes = Blueprint("pointset_manager_routes", __name__)

_pointset_storage: Dict[str, bytes] = {}

def create_pointset():
    donnees_binaires = request.data
    if not donnees_binaires:
        return jsonify({"code": "INVALID_DATA", "message": "Aucune donnée fournie"}), 400

    try:
        from triangulator.usecases.PointSet import PointSet as ps
        points = ps.parse_pointset(donnees_binaires)
    except Exception:
        return jsonify({"code": "INVALID_FORMAT", "message": "Format binaire invalide"}), 400

    identifiant = str(uuid.uuid4())

    _pointset_storage[identifiant] = donnees_binaires

    return jsonify({"pointSetId": identifiant}), 201

def get_pointset_by_id(identifiant_pointset: str):
    try:
        uuid.UUID(identifiant_pointset)
    except ValueError:
        return jsonify({"code": "INVALID_ID", "message": "Format d'ID invalide"}), 400

    if identifiant_pointset not in _pointset_storage:
        return b"", 404

    return _pointset_storage[identifiant_pointset], 200

@pointset_routes.post("/pointset")
def enregistrer_pointset():
    module = importlib.import_module(__name__)
    return module.create_pointset()

@pointset_routes.get("/pointset/<string:pointset_id>")
def recuperer_pointset_par_id(pointset_id: str):
    module = importlib.import_module(__name__)
    donnees, statut = module.get_pointset_by_id(pointset_id)
    return Response(donnees, status=statut, mimetype="application/octet-stream")
