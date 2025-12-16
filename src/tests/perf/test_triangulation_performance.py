import time
import random
import pytest
from triangulator.usecases.Triangles import Triangles

@pytest.mark.slow
@pytest.mark.parametrize("num_points", [10, 100, 1000, 10000])
def test_triangulation_performance(num_points):
    random.seed(42)  # Pour des résultats reproductibles
    points = [(random.random(), random.random()) for _ in range(num_points)]

    # Mesurer le temps d'exécution
    start_time = time.perf_counter()
    triangles = Triangles.triangulate_delaunay(points)
    end_time = time.perf_counter()

    execution_time = end_time - start_time

    if num_points >= 3:
        assert len(triangles) > 0, f"Aucun triangle généré pour {num_points} points"
    else:
        assert len(triangles) == 0, f"Triangles générés pour {num_points} points alors qu'il ne devrait pas y en avoir"

    print(f"Temps d'exécution: {execution_time:.6f}s")
    print(f"Nombre de triangles générés: {len(triangles)}")

    if num_points <= 1000:
        assert execution_time < 1.0, f"Temps d'exécution trop long pour {num_points} points: {execution_time:.6f}s"
    elif num_points <= 10000:
        assert execution_time < 10.0, f"Temps d'exécution trop long pour {num_points} points: {execution_time:.6f}s"