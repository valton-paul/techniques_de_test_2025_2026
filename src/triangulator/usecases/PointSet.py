import struct
from typing import List, Tuple, Union, Any


class PointSet:

    points: List[Tuple[float, float]]
    
    def __init__(self, points: List[Tuple[float, float]]):
        if not isinstance(points, list):
            raise TypeError("points doit être une liste")
        for i, point in enumerate(points):
            if not isinstance(point, (tuple, list)) or len(point) != 2:
                raise ValueError(f"Point {i} invalide: {point}")
            x, y = point
            if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                raise TypeError(f"Coordonnées invalides pour le point {i}: {point}")
        self.points = points


    @staticmethod
    def parse_pointset(binary_data: bytes) -> 'PointSet':
        if len(binary_data) < 4:
            raise ValueError("insufficient data")

        (num_points,) = struct.unpack_from("<L", binary_data, 0)
        expected_size = 4 + (8 * num_points)
        if len(binary_data) != expected_size:
            raise ValueError("invalid data size")

        points_list: List[Tuple[float, float]] = []
        offset = 4
        for _ in range(num_points):
            x, y = struct.unpack_from("<ff", binary_data, offset)
            points_list.append((x, y))
            offset += 8

        return PointSet(points_list)

    @staticmethod
    def serialize_pointset(points: 'PointSet') -> bytes:
        points_to_serialize = points.points

        data = struct.pack("<L", len(points_to_serialize))
        for point in points_to_serialize:
            x, y = point
            data += struct.pack("<ff", float(x), float(y))

        return data