import pytest

import fuzzy_logic as fl

# test cases for the tests of piecewise membership function
PIECEWISE_IDS = [
    'rectangle',
    'right triangle - right',
    'right triangle - left',
    'triangle',
    'right trapezoid - right',
    'right trapezoid - left',
    'trapezoid',
    'complex'
]
PIECEWISE_MASSES = [1, 1/2, 1/2, 3/2, 3/2, 3/2, 7/2, 19/4]
PIECEWISE_CENTERS = [1, 4/3, 2/3, 5/3, 22/9, 14/9, 57/21, 176/57]
PIECEWISE_SHAPES = [
    [(0.0, 0.5), (2.0, 0.5)],
    [(0.0, 0.0), (2.0, 0.5)],
    [(0.0, 0.5), (2.0, 0.0)],
    [(0.0, 0.0), (2.0, 1.0), (3.0, 0.0)],
    [(0.0, 0.0), (2.0, 0.5), (4.0, 0.5)],
    [(0.0, 0.5), (2.0, 0.5), (4.0, 0.0)],
    [(0.0, 0.0), (2.0, 1.0), (4.0, 1.0), (5.0, 0.0)],
    [(0.0, 1.0), (1.0, 1.0), (2.0, 0.5), (3.0, 0.5), (5.0, 1.0), (7.0, 0.0)]
]


def test_piecewise_2_points():
    """ Tests a interpolation of a two-points piecewise membership function. """
    membership = fl.PiecewiseMembership([(0.0, 1.0), (1.0, 0.5)])
    expected = [
        (-10.0, 0.0), (1.1, 0.0),  # outside
        (0.0, 1.0), (1.0, 0.5),  # points
        (0.1, 0.95), (0.5, 0.75)  # inside
    ]

    for x, y in expected:
        assert membership(x) == y


def test_piecewise_3_points():
    """ Tests a interpolation of a three-points piecewise membership function. """
    membership = fl.PiecewiseMembership([(0.0, 1.0), (1.0, 0.5), (1.5, 1.0)])
    expected = [
        (-10.0, 0.0), (1.6, 0.0),  # outside
        (0.0, 1.0), (1.0, 0.5), (1.5, 1.0),  # points
        (0.1, 0.95), (0.5, 0.75), (1.25, 0.75)  # inside
    ]

    for x, y in expected:
        assert membership(x) == y


@pytest.mark.parametrize(
    argnames=['points', 'center'],
    argvalues=list(zip(PIECEWISE_SHAPES, PIECEWISE_CENTERS)),
    ids=PIECEWISE_IDS
)
def test_piecewise_center(points, center):
    """ Tests the center-of-mass calculation of a piecewise membership function. """
    assert fl.PiecewiseMembership(points).center == pytest.approx(center)


@pytest.mark.parametrize(
    argnames=['points', 'mass'],
    argvalues=list(zip(PIECEWISE_SHAPES, PIECEWISE_MASSES)),
    ids=PIECEWISE_IDS
)
def test_piecewise_mass(points, mass):
    """ Tests the mass calculation for a piecewise membership function. """
    assert fl.PiecewiseMembership(points).mass == pytest.approx(mass)


def test_triangular():
    """ Tests the membership function in a form of a triangle. """
    membership = fl.TriangularMembership(0.0, 2.0, 3.0)
    expected = [
        (-10.0, 0.0), (3.1, 0.0),  # outside
        (0.0, 0.0), (2.0, 1.0), (3.0, 0.0),  # points
        (0.5, 0.25), (1.0, 0.5), (2.25, 0.75)  # inside
    ]

    for x, y in expected:
        assert membership(x) == y


def test_trapezoidal():
    """ Tests the membership function in a form of a (not right) trapezoidal. """
    membership = fl.TrapezoidalMembership(0.0, 2.0, 3.0, 4.0)
    expected = [
        (-10.0, 0.0), (4.1, 0.0),  # outside
        (0.0, 0.0), (2.0, 1.0), (3.0, 1.0), (4.0, 0.0),  # points
        (0.5, 0.25), (1.0, 0.5), (2.25, 1.0), (3.5, 0.5)  # inside
    ]

    for x, y in expected:
        assert membership(x) == y


def test_trapezoidal_left():
    """ Tests the membership function in a form of a right trapezoidal with right angle at lower x-coordinates. """
    membership = fl.TrapezoidalMembership(None, 2.0, 3.0, 4.0)
    expected = [
        (1.9, 0.0), (4.1, 0.0),  # outside
        (2.0, 1.0), (3.0, 1.0), (4.0, 0.0),  # points
        (2.25, 1.0), (3.5, 0.5)  # inside
    ]

    for x, y in expected:
        assert membership(x) == y


def test_trapezoidal_right():
    """ Tests the membership function in a form of a right trapezoidal with right angle at higher x-coordinates. """
    membership = fl.TrapezoidalMembership(1.0, 2.0, 3.0, None)
    expected = [
        (0.9, 0.0), (3.1, 0.0),  # outside
        (1.0, 0.0), (2.0, 1.0), (3.0, 1.0),  # points
        (1.5, 0.5), (2.5, 1.0)  # inside
    ]

    for x, y in expected:
        assert membership(x) == y


def test_trapezoidal_rectangle():
    """ Tests the membership function in a form of a rectangle. """
    membership = fl.TrapezoidalMembership(None, 2.0, 3.0, None)
    expected = [
        (1.9, 0.0), (3.1, 0.0),  # outside
        (2.0, 1.0), (3.0, 1.0),  # points
        (2.5, 1.0),  # inside
    ]

    for x, y in expected:
        assert membership(x) == y
