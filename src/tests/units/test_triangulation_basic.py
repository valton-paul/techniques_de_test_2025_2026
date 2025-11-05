import struct
from triangulator.Triangles import Triangles as tr

def test_minimal_triangle(): 
    point_count = struct.pack("<L", 3)
    point1 = struct.pack("<ff", 0.0, 0.0)
    point2 = struct.pack("<ff", 1.0, 0.0)
    point3 = struct.pack("<ff", 0.0, 1.0)
    triangle_count = struct.pack("<L", 1)
    triangle1 = struct.pack("<LLL", 0, 1, 2)

    triangle_bytes = point_count + point1 + point2 + point3 + triangle_count + triangle1

    expected_points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    expected_triangles = [(0, 1, 2)]

    result = tr.parse_triangles(triangle_bytes)

    assert result.points == expected_points
    assert result.triangles == expected_triangles

def test_square_case(): 
    point_count = struct.pack("<L", 4)
    point1 = struct.pack("<ff", 0.0, 0.0)
    point2 = struct.pack("<ff", 1.0, 0.0)
    point3 = struct.pack("<ff", 1.0, 1.0)
    point4 = struct.pack("<ff", 0.0, 1.0)
    triangle_count = struct.pack("<L", 2)
    triangle1 = struct.pack("<LLL", 0, 1, 2)
    triangle2 = struct.pack("<LLL", 0, 2, 3)

    triangle_bytes = (point_count + point1 + point2 + point3 + point4 +
                      triangle_count + triangle1 + triangle2)

    expected_points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    expected_triangles = [(0, 1, 2), (0, 2, 3)]

    result = tr.parse_triangles(triangle_bytes)

    assert result.points == expected_points
    assert result.triangles == expected_triangles