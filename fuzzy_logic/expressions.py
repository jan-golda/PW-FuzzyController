from __future__ import annotations

from abc import ABC, abstractmethod
from typing import NamedTuple, Set

from matplotlib.patches import Patch

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

    @property
    @abstractmethod
    def terms(self) -> Set[Term]:
        """ Terms used in this expression. """


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

    @property
    def terms(self) -> Set[Term]:
        return {self}

    @property
    def plt_patch(self) -> Patch:
        """ Matplotlib patch in a shape of this var membership function. """
        patch = self.membership.plt_patch
        patch.set_label(self.label)
        return patch


class UnaryExpression(Expression, ABC):
    """ Base class for all unary expressions. """
    def __init__(self, expr: Expression):
        self._expr = expr

    @property
    def terms(self) -> Set[Term]:
        return self._expr.terms


class BinaryExpression(Expression, ABC):
    """ Base class for all binary expressions. """
    def __init__(self, left: Expression, right: Expression):
        self._left = left
        self._right = right

    @property
    def terms(self) -> Set[Term]:
        return self._left.terms | self._right.terms


class NotExpression(UnaryExpression):
    """ Represents a logical negation. """
    def __call__(self, **inputs: float) -> float:
        return 1 - self._expr(**inputs)


class AndExpression(BinaryExpression):
    """ Represents a logical conjunction. """
    def __call__(self, **inputs: float) -> float:
        return min(self._left(**inputs), self._right(**inputs))


class OrExpression(BinaryExpression):
    """ Represents a logical disjunction. """
    def __call__(self, **inputs: float) -> float:
        return max(self._left(**inputs), self._right(**inputs))


class Rule(NamedTuple):
    """ Represents a fuzzy logic rule. """
    antecedent: Expression
    consequent: Term
