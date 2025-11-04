import math
import struct

def test_parse_pointset_valid():
    point_count = struct.pack("<L", 2)
    point1 = struct.pack("<ff", 1.0, 2.0) 
    point2 = struct.pack("<ff", -3.0, 4.5)
    valid_bytes = point_count + point1 + point2

    expected = [(1.0, 2.0), (-3.0, 4.5)]

    # WHEN
    from triangulator.binary import parse_pointset
    result = parse_pointset(valid_bytes)

    # THEN
    assert len(result) == len(expected)
    for (x_exp, y_exp), (x_res, y_res) in zip(expected, result):
        assert math.isclose(x_exp, x_res)
        assert math.isclose(y_exp, y_res)

def test_parse_pointset_too_short():
    point_count = struct.pack("<L", 3)
    point1 = struct.pack("<ff", 1.0, 2.0)
    point2 = struct.pack("<ff", -3.0, 4.5)
    invalid_bytes = point_count + point1 + point2

    # WHEN
    from triangulator.binary import parse_pointset
    try:
        parse_pointset(invalid_bytes)
        assert False, "Expected an exception for too short data"
    except Exception as e:
        # THEN
        assert isinstance(e, ValueError)
    
def test_parse_empty_pointset():
    point_count = struct.pack("<L", 0)
    empty_bytes = point_count

    expected = []

    # WHEN
    from triangulator.binary import parse_pointset
    result = parse_pointset(empty_bytes)

    # THEN
    assert result == expected

def test_parse_too_long_pointset():
    point_count = struct.pack("<L", 1)
    point1 = struct.pack("<ff", 1.0, 2.0)
    point2 = struct.pack("<ff", -3.0, 4.5)
    invalid_bytes = point_count + point1 + point2

    # WHEN
    from triangulator.binary import parse_pointset
    try:
        parse_pointset(invalid_bytes)
        assert False, "Expected an exception for too long data"
    except Exception as e:
        # THEN
        assert isinstance(e, ValueError)