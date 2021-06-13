from __future__ import annotations

from abc import ABC, abstractmethod


class Expression(ABC):
    """ Base class for fuzzy expression. """

    @abstractmethod
    def __call__(self, **inputs: float) -> float:
        """ Evaluates the expression for given inputs. """

    def __invert__(self) -> NotExpression:
        """ Overloads `~` operator so that you can express logical negation as `~A`. """
        return NotExpression(self)

    def __and__(self, other: Expression) -> AndExpression:
        """ Overloads `&` operator so that you can express logical conjunction as `A & B`. """
        assert isinstance(other, Expression)
        return AndExpression(self, other)

    def __or__(self, other: Expression) -> OrExpression:
        """ Overloads `|` operator so that you can express logical disjunction as `A | B`. """
        assert isinstance(other, Expression)
        return OrExpression(self, other)


class NotExpression(Expression):
    """ Represents a logical negation. """
    def __init__(self, expr: Expression):
        self._expr = expr

    def __call__(self, **inputs: float) -> float:
        return 1 - self._expr(**inputs)


class AndExpression(Expression):
    """ Represents a logical conjunction. """
    def __init__(self, left: Expression, right: Expression):
        self._left = left
        self._right = right

    def __call__(self, **inputs: float) -> float:
        return min(self._left(**inputs), self._right(**inputs))


class OrExpression(Expression):
    """ Represents a logical disjunction. """
    def __init__(self, left: Expression, right: Expression):
        self._left = left
        self._right = right

    def __call__(self, **inputs: float) -> float:
        return max(self._left(**inputs), self._right(**inputs))
