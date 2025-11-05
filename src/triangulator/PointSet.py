class PointSet:
    
    def __init__(self, points: list[tuple[float, float]]):
        self.points = points


    @staticmethod
    def parse_pointset(data: bytes) -> list[tuple[float, float]]:
        raise NotImplementedError("parse_pointset pas encore implémentée")

    @staticmethod
    def serialize_pointset(points: list[tuple[float, float]]) -> bytes:
        raise NotImplementedError("serialize_pointset pas encore implémentée")