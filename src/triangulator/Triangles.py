from .PointSet import PointSet as PointSet

class Triangles:
    
    points: PointSet
    triangles: list[tuple[int, int, int]]

    def __init__(self, points: PointSet, triangles: list[tuple[int, int, int]]):
        self.points = [] if points is None else points
        self.triangles = [] if triangles is None else triangles
    
    @staticmethod
    def parse_triangles(data: bytes) -> 'Triangles':
        raise NotImplementedError("parse_triangles pas encore implémentée")
    
    @staticmethod
    def serialize_triangles(triangles: 'Triangles') -> bytes:
        raise NotImplementedError("serialize_triangles pas encore implémentée")