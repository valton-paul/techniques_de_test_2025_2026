class PointSet:

    points: list[tuple[float, float]]
    
    def __init__(self, points: list[tuple[float, float]]):
        self.points = points


    @staticmethod
    def parse_pointset(data: bytes) -> 'PointSet':
        raise NotImplementedError("parse_pointset pas encore implémentée")

    @staticmethod
    def serialize_pointset(points: 'PointSet') -> bytes:
        raise NotImplementedError("serialize_pointset pas encore implémentée")