
import importlib
import uuid
from flask import Blueprint, Response, jsonify
from triangulator.usecases.Triangles import Triangles
from triangulator.usecases.PointSet import PointSet

triangulation_routes = Blueprint("triangulation_routes", __name__)

def _get_pointset_data(pointset_id: str) -> bytes:
    pointset_module = importlib.import_module("triangulator.routes.pointset_routes")
    donnees, statut = pointset_module.get_pointset_by_id(pointset_id)

    if statut == 404:
        raise ValueError(f"PointSet non trouvé: {pointset_id}")

    return donnees


def get_triangulation(identifiant_pointset: str) -> bytes:
    try:
        uuid.UUID(identifiant_pointset)
    except ValueError:
        raise ValueError(f"Format UUID invalide: {identifiant_pointset}")

    pointset_data = _get_pointset_data(identifiant_pointset)

    try:
        pointset = PointSet.parse_pointset(pointset_data)
    except Exception as e:
        raise RuntimeError(f"Erreur lors du parsing du pointset: {str(e)}")

    try:
        # Delaunay triangulation using Bowyer-Watson algorithm
        indices_triangles = Triangles.triangulate_delaunay(pointset.points)

        triangles = Triangles(pointset, indices_triangles)
        return Triangles.serialize_triangles(triangles)

    except Exception as e:
        raise RuntimeError(f"Échec de la triangulation: {str(e)}")


@triangulation_routes.get("/triangulation/<string:pointset_id>")
def recuperer_triangulation(pointset_id: str):
    try:
        module = importlib.import_module(__name__)
        donnees_binaires = module.get_triangulation(pointset_id)
        return Response(donnees_binaires, status=200, mimetype="application/octet-stream")
        
    except ValueError as e:
        if "Format UUID invalide" in str(e):
            return jsonify({
                "code": "INVALID_UUID",
                "message": str(e)
            }), 400
        elif "PointSet non trouvé" in str(e):
            return jsonify({
                "code": "POINTSET_NOT_FOUND",
                "message": str(e)
            }), 404
        else:
            return jsonify({
                "code": "BAD_REQUEST",
                "message": str(e)
            }), 400

    except RuntimeError as e:
        return jsonify({
            "code": "TRIANGULATION_FAILED",
            "message": str(e)
        }), 500
        
    except Exception as e:
        return jsonify({
            "code": "INTERNAL_ERROR",
            "message": "Une erreur inattendue s'est produite"
        }), 500

