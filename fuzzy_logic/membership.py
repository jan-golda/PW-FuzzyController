from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


class Membership(ABC):
    """ Interface for all membership functions. """

    @abstractmethod
    def __call__(self, value: float) -> float:
        """ Calculates the membership for the given input value. """

    @property
    @abstractmethod
    def center(self) -> float:
        """ X coordinate of the center of the mass of area under this membership function. """

    @property
    @abstractmethod
    def mass(self) -> float:
        """ Mass of the area under this membership function. """

    @property
    @abstractmethod
    def plt_patch(self):
        """ Matplotlib patch in a shape of this membership function. """


class PiecewiseMembership(Membership):
    """ Defines membership function as a piecewise linear function. """
    def __init__(self, points: List[Tuple[float, float]]):
        self._points = sorted(points)

    def __call__(self, value: float) -> float:
        p = self._points
        for i in range(len(p) - 1):
            if p[i][0] <= value <= p[i+1][0]:
                return p[i][1] + (p[i+1][1] - p[i][1]) * (value - p[i][0]) / (p[i+1][0] - p[i][0])
        return 0.0

    @property
    def center(self) -> float:
        centers = list(map(self._segment_center, range(len(self._points) - 1)))
        masses = list(map(self._segment_mass, range(len(self._points) - 1)))
        return sum(c * m for c, m in zip(centers, masses)) / sum(masses)

    @property
    def mass(self) -> float:
        return sum(map(self._segment_mass, range(len(self._points) - 1)))

    def _segment_center(self, i: int) -> float:
        """ X coordinate of the center of mass of i-th segment. """
        p1, p2 = self._points[i:i+2]

        rectangle_center = (p2[0] + p1[0]) / 2.0
        rectangle_mass = (p2[0] - p1[0]) * min(p1[1], p2[1])
        triangle_center = (p1[0] + p2[0] + (p1[0] if p1[1] > p2[1] else p2[0])) / 3.0
        triangle_mass = (p2[0] - p1[0]) * (max(p1[1], p2[1]) - min(p1[1], p2[1])) / 2.0

        return (rectangle_center * rectangle_mass + triangle_center * triangle_mass) / (rectangle_mass + triangle_mass)

    def _segment_mass(self, i: int) -> float:
        """ Mass of the i-th segment. """
        p1, p2 = self._points[i:i+2]
        return (p1[1] + p2[1]) / 2.0 * (p2[0] - p1[0])

    @property
    def plt_patch(self):
        from matplotlib.patches import Polygon
        return Polygon(
            [(self._points[0][0], 0.0)] + self._points + [(self._points[-1][0], 0.0)]
        )


class TriangularMembership(PiecewiseMembership):
    """ Defines membership function in a shape of a triangle. """
    def __init__(self, val_min: float, val_mid: float, val_max: float):
        super().__init__([(val_min, 0.0), (val_mid, 1.0), (val_max, 0.0)])


class TrapezoidalMembership(PiecewiseMembership):
    """ Defines membership function in a shape of a trapezoid. """
    def __init__(self, val_min: Optional[float], val_mid_low: float, val_mid_high: float, val_max: Optional[float]):
        points = [(val_mid_low, 1.0), (val_mid_high, 1.0)]
        if val_min is not None:
            points = [(val_min, 0.0)] + points
        if val_max is not None:
            points = points + [(val_max, 0.0)]
        super().__init__(points)
