import struct
from triangulator.usecases.Triangles import Triangles as tr
from triangulator.usecases.PointSet import PointSet

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

    assert result.points.points == expected_points
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

    assert result.points.points == expected_points
    assert result.triangles == expected_triangles

def test_invalid_triangle_data(): 
    point_count = struct.pack("<L", 3)
    point1 = struct.pack("<ff", 0.0, 0.0)
    point2 = struct.pack("<ff", 1.0, 0.0)
    point3 = struct.pack("<ff", 0.0, 1.0)
    triangle_count = struct.pack("<L", 1)
    invalid_triangle = struct.pack("<LL", 0, 1)  # On oublie le troisième index

    invalid_bytes = (point_count + point1 + point2 + point3 +
                     triangle_count + invalid_triangle)

    try:
        tr.parse_triangles(invalid_bytes)
        assert False
    except ValueError:
        assert True

def test_serialize_minimal_triangle(): 
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = [(0, 1, 2)]

    expected_bytes = (struct.pack("<Lff", 3, 0.0, 0.0) +
                      struct.pack("<ff", 1.0, 0.0) +
                      struct.pack("<ff", 0.0, 1.0) +
                      struct.pack("<L", 1) +
                      struct.pack("<LLL", 0, 1, 2))

    result_bytes = tr.serialize_triangles(tr(PointSet(points), triangles))

    assert result_bytes == expected_bytes

def test_serialize_square_case(): 
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    triangles = [(0, 1, 2), (0, 2, 3)]

    expected_bytes = (struct.pack("<Lff", 4, 0.0, 0.0) +
                      struct.pack("<ff", 1.0, 0.0) +
                      struct.pack("<ff", 1.0, 1.0) +
                      struct.pack("<ff", 0.0, 1.0) +
                      struct.pack("<L", 2) +
                      struct.pack("<LLL", 0, 1, 2) +
                      struct.pack("<LLL", 0, 2, 3))

    result_bytes = tr.serialize_triangles(tr(PointSet(points), triangles))

    assert result_bytes == expected_bytes

def test_serialize_empty_triangles(): 
    points = []
    triangles = []

    expected_bytes = struct.pack("<L", 0) + struct.pack("<L", 0)

    result_bytes = tr.serialize_triangles(tr(PointSet(points), triangles))

    assert result_bytes == expected_bytes

