from .PointSet import PointSet
import struct
import math
from typing import List, Tuple, Set


class Triangles:    
    points: PointSet
    triangles: list[tuple[int, int, int]]

    def __init__(self, points: PointSet, triangles: list[tuple[int, int, int]]):

        for i, triangle in enumerate(triangles):
            if not isinstance(triangle, (tuple, list)) or len(triangle) != 3:
                raise ValueError(f"Triangle {i} invalide: {triangle}")
            a, b, c = triangle
            if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int):
                raise TypeError(f"Indices invalides pour le triangle {i}: {triangle}")
            max_index = len(points.points) - 1
            if not (0 <= a <= max_index and 0 <= b <= max_index and 0 <= c <= max_index):
                raise ValueError(f"Indices hors limites pour le triangle {i}: {triangle}")

        self.points = points
        self.triangles = triangles

    @staticmethod
    def triangulate_delaunay(points: List[Tuple[float, float]]) -> List[Tuple[int, int, int]]:
        n = len(points)
        if n < 3:
            return []
        elif n == 3:
            # Vérifier si les 3 points sont colinéaires
            p1, p2, p3 = points
            area = abs((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])) / 2
            if area < 1e-10:
                # Points colinéaires - pas de triangle valide
                return []
            return [(0, 1, 2)]

        import numpy as np
        from scipy.spatial import Delaunay

        # Convertir en numpy array
        points_array = np.array(points)

        tri = Delaunay(points_array)

        # Convertir les simplexes en liste de tuples et filtrer les triangles dégénérés
        triangles = []
        for simplex in tri.simplices:
            # Calculer l'aire du triangle pour vérifier qu'il n'est pas dégénéré
            p1, p2, p3 = [points_array[i] for i in simplex]
            # Formule de l'aire d'un triangle en 2D
            area = abs((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])) / 2

            # Ne garder que les triangles avec une aire significative (> tolérance)
            if area > 1e-10:
                triangles.append(tuple(simplex))

        return triangles

    @staticmethod
    def parse_triangles(binary_data: bytes) -> 'Triangles':
        if len(binary_data) < 8:
            raise ValueError("insufficient data")

        (num_points,) = struct.unpack_from("<L", binary_data, 0)
        points_size = 4 + (8 * num_points)
        if len(binary_data) < points_size + 4:
            raise ValueError("insufficient data")

        vertices = PointSet.parse_pointset(binary_data[:points_size])

        (num_triangles,) = struct.unpack_from("<L", binary_data, points_size)
        expected_size = points_size + 4 + (12 * num_triangles)
        if len(binary_data) != expected_size:
            raise ValueError("invalid data size")

        triangle_list: list[tuple[int, int, int]] = []
        offset = points_size + 4
        for _ in range(num_triangles):
            a, b, c = struct.unpack_from("<LLL", binary_data, offset)
            triangle_list.append((int(a), int(b), int(c)))
            offset += 12

        return Triangles(vertices, triangle_list)
    
    @staticmethod
    def serialize_triangles(triangles: 'Triangles') -> bytes:

        data = PointSet.serialize_pointset(triangles.points)
        data += struct.pack("<L", len(triangles.triangles))

        for triangle in triangles.triangles:
            a, b, c = triangle
            data += struct.pack("<LLL", a, b, c)

        return data