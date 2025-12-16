import math
import struct
from triangulator.usecases.PointSet import PointSet as ps

def test_parse_pointset_valid():
    point_count = struct.pack("<L", 2)
    point1 = struct.pack("<ff", 1.0, 2.0) 
    point2 = struct.pack("<ff", -3.0, 4.5)
    valid_bytes = point_count + point1 + point2

    expected = [(1.0, 2.0), (-3.0, 4.5)]

    result = ps.parse_pointset(valid_bytes)

    assert len(result.points) == len(expected)
    for (x_exp, y_exp), (x_res, y_res) in zip(expected, result.points):
        assert math.isclose(x_exp, x_res)
        assert math.isclose(y_exp, y_res)

def test_parse_large_pointset():
    point_count = 1000
    points = [(float(i), float(i) * 2.0) for i in range(point_count)]
    
    byte_data = struct.pack("<L", point_count)
    for x, y in points:
        byte_data += struct.pack("<ff", x, y)

    result = ps.parse_pointset(byte_data)

    assert len(result.points) == point_count
    for (x_exp, y_exp), (x_res, y_res) in zip(points, result.points):
        assert math.isclose(x_exp, x_res)
        assert math.isclose(y_exp, y_res)

def test_parse_pointset_too_short():
    point_count = struct.pack("<L", 3)
    point1 = struct.pack("<ff", 1.0, 2.0)
    point2 = struct.pack("<ff", -3.0, 4.5)
    invalid_bytes = point_count + point1 + point2

    try:
        ps.parse_pointset(invalid_bytes)
        assert False
    except ValueError:
        assert True

def test_parse_pointset_invalid_count():
    invalid_bytes = struct.pack("<L", 2) + struct.pack("<f", 1.0) + struct.pack("<f", 1.5) + struct.pack("<f", 2.5)

    try:
        ps.parse_pointset(invalid_bytes)
        assert False
    except ValueError:
        assert True
    
def test_parse_empty_pointset():
    point_count = struct.pack("<L", 0)
    empty_bytes = point_count

    expected = []
    
    result = ps.parse_pointset(empty_bytes)

    assert result.points == expected

def test_parse_too_long_pointset():
    point_count = struct.pack("<L", 1)
    point1 = struct.pack("<ff", 1.0, 2.0)
    point2 = struct.pack("<ff", -3.0, 4.5)
    invalid_bytes = point_count + point1 + point2
    
    try:
        ps.parse_pointset(invalid_bytes)
        assert False
    except ValueError:
        assert True

def test_serialize_pointset():
    points = [(1.0, 2.0), (-3.0, 4.5)]
    pointset = ps(points)

    expected_bytes = struct.pack("<Lff", 2, 1.0, 2.0) + struct.pack("<ff", -3.0, 4.5)

    result_bytes = ps.serialize_pointset(pointset)

    assert result_bytes == expected_bytes

def test_serialize_empty_pointset():
    points = []
    pointset = ps(points)

    expected_bytes = struct.pack("<L", 0)

    result_bytes = ps.serialize_pointset(pointset)

    assert result_bytes == expected_bytes

def test_serialize_single_point_pointset():
    points = [(3.14, -2.71)]
    pointset = ps(points)

    expected_bytes = struct.pack("<Lff", 1, 3.14, -2.71)

    result_bytes = ps.serialize_pointset(pointset)

    assert result_bytes == expected_bytes

def test_serialize_wrong_point_format():
    points = [(1.0, 2.0, 3.0)]

    try:
        pointset = ps(points)
        assert False
    except ValueError:
        assert True

def test_serialize_non_float_point():
    points = [(1.0, "a")]

    try:
        pointset = ps(points)
        assert False
    except TypeError:
        assert True