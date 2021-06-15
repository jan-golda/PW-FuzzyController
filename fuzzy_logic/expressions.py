from __future__ import annotations

from abc import ABC, abstractmethod
from typing import NamedTuple

from fuzzy_logic import Membership


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

    def __rshift__(self, other: Term) -> Rule:
        """ Overloads `>>` operator so that you can express logical implication as `A >> B`. """
        assert isinstance(other, Term)
        return Rule(self, other)


class Term(Expression):
    """ Represents a fuzzy term defined for a given membership function. """

    def __init__(self, variable: str, label: str, membership: Membership):
        self._variable = variable
        self._label = label
        self._membership = membership

    def __call__(self, **inputs: float) -> float:
        return self._membership(inputs[self._variable])

    @property
    def variable(self) -> str:
        return self._variable

    @property
    def label(self) -> str:
        return self._label

    @property
    def membership(self) -> Membership:
        return self._membership


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


class Rule(NamedTuple):
    """ Represents a fuzzy logic rule. """
    antecedent: Expression
    consequent: Term
