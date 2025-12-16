import pytest
from triangulator.usecases.Triangles import Triangles


def test_triangulation_no_self_intersections():
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    triangles = Triangles.triangulate_delaunay(points)

    for triangle in triangles:
        assert len(triangle) == 3, f"Triangle invalide: {triangle}"
        assert len(set(triangle)) == 3, f"Triangle avec indices dupliqués: {triangle}"
        for idx in triangle:
            assert 0 <= idx < len(points), f"Index hors limites: {idx}"

    assert len(triangles) == 2, f"Nombre de triangles inattendu: {len(triangles)}"


def test_triangulation_all_points_used():
    points = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0), (0.5, 0.5), (1.5, 0.5)]
    triangles = Triangles.triangulate_delaunay(points)

    used_indices = set()
    for triangle in triangles:
        used_indices.update(triangle)

    expected_indices = set(range(len(points)))
    assert used_indices == expected_indices, f"Points non utilisés: {expected_indices - used_indices}"


def test_triangulation_edge_cases():

    points = [(0.0, 0.0), (1.0, 1.0)]
    triangles = Triangles.triangulate_delaunay(points)
    assert len(triangles) == 0, "2 points ne devraient pas produire de triangles"

    points = [(0.0, 0.0)]
    triangles = Triangles.triangulate_delaunay(points)
    assert len(triangles) == 0, "1 point ne devrait pas produire de triangles"

    points = []
    triangles = Triangles.triangulate_delaunay(points)
    assert len(triangles) == 0, "0 points ne devraient pas produire de triangles"

def test_collinear_points():
    """
    Test that 3 perfectly collinear points should not produce any valid triangles.
    In Delaunay triangulation, collinear points should not form degenerate triangles.
    """
    # Points perfectly aligned on a line
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]
    triangles = Triangles.triangulate_delaunay(points)

    # Should produce no triangles since points are collinear
    assert len(triangles) == 0, f"3 points alignés devraient produire 0 triangles, obtenu {len(triangles)}"
