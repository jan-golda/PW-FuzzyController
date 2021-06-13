from abc import ABC, abstractmethod
from typing import List, Tuple


class Membership(ABC):

    @abstractmethod
    def __call__(self, value: float) -> float:
        """ Calculates the membership for the given input value. """


class PiecewiseMembership(Membership):
    """ Defines membership function as a piecewise linear function. """
    def __init__(self, points: List[Tuple[float, float]]):
        self._points = sorted(points)

    def __call__(self, value: float) -> float:
        for i in range(len(self._points) - 1):
            if self._points[i][0] <= value <= self._points[i+1][0]:
                return self._points[i][1] + (self._points[i+1][1] - self._points[i][1]) * (value - self._points[i][0]) / (self._points[i+1][0] - self._points[i][0])
        return 0.0


class TriangularMembership(PiecewiseMembership):
    """ Defines membership function in a shape of a triangle. """
    def __init__(self, val_min: float, val_mid: float, val_max: float):
        super().__init__([(val_min, 0.0), (val_mid, 1.0), (val_max, 0.0)])


class TrapezoidalMembership(PiecewiseMembership):
    """ Defines membership function in a shape of a trapezoid. """
    def __init__(self, val_min: float, val_mid_low: float, val_mid_high: float, val_max: float):
        super().__init__([(val_min, 0.0), (val_mid_low, 1.0), (val_mid_high, 1.0), (val_max, 0.0)])
