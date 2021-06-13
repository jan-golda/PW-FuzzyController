import fuzzy_logic as fl


def test_piecewise_2_points():
    membership = fl.PiecewiseMembership([(0.0, 1.0), (1.0, 0.5)])
    expected = [
        (-10.0, 0.0), (1.1, 0.0),  # outside
        (0.0, 1.0), (1.0, 0.5),  # points
        (0.1, 0.95), (0.5, 0.75)  # inside
    ]

    for x, y in expected:
        assert membership(x) == y


def test_piecewise_3_points():
    membership = fl.PiecewiseMembership([(0.0, 1.0), (1.0, 0.5), (1.5, 1.0)])
    expected = [
        (-10.0, 0.0), (1.6, 0.0),  # outside
        (0.0, 1.0), (1.0, 0.5), (1.5, 1.0),  # points
        (0.1, 0.95), (0.5, 0.75), (1.25, 0.75)  # inside
    ]

    for x, y in expected:
        assert membership(x) == y


def test_triangular():
    membership = fl.TriangularMembership(0.0, 2.0, 3.0)
    expected = [
        (-10.0, 0.0), (3.1, 0.0),  # outside
        (0.0, 0.0), (2.0, 1.0), (3.0, 0.0),  # points
        (0.5, 0.25), (1.0, 0.5), (2.25, 0.75)  # inside
    ]

    for x, y in expected:
        assert membership(x) == y


def test_trapezoidal():
    membership = fl.TrapezoidalMembership(0.0, 2.0, 3.0, 4.0)
    expected = [
        (-10.0, 0.0), (4.1, 0.0),  # outside
        (0.0, 0.0), (2.0, 1.0), (3.0, 1.0), (4.0, 0.0),  # points
        (0.5, 0.25), (1.0, 0.5), (2.25, 1.0), (3.5, 0.5)  # inside
    ]

    for x, y in expected:
        assert membership(x) == y


def test_trapezoidal_left():
    membership = fl.TrapezoidalMembership(None, 2.0, 3.0, 4.0)
    expected = [
        (1.9, 0.0), (4.1, 0.0),  # outside
        (2.0, 1.0), (3.0, 1.0), (4.0, 0.0),  # points
        (2.25, 1.0), (3.5, 0.5)  # inside
    ]

    for x, y in expected:
        assert membership(x) == y


def test_trapezoidal_right():
    membership = fl.TrapezoidalMembership(1.0, 2.0, 3.0, None)
    expected = [
        (0.9, 0.0), (3.1, 0.0),  # outside
        (1.0, 0.0), (2.0, 1.0), (3.0, 1.0),  # points
        (1.5, 0.5), (2.5, 1.0)  # inside
    ]

    for x, y in expected:
        assert membership(x) == y


def test_trapezoidal_rectangle():
    membership = fl.TrapezoidalMembership(None, 2.0, 3.0, None)
    expected = [
        (1.9, 0.0), (3.1, 0.0),  # outside
        (2.0, 1.0), (3.0, 1.0),  # points
        (2.5, 1.0),  # inside
    ]

    for x, y in expected:
        assert membership(x) == y
