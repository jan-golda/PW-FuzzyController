""" Module that implements a generic fuzzy logic system. """
from .membership import Membership, PiecewiseMembership, TriangularMembership, TrapezoidalMembership
from .expressions import Expression, Term, Rule, NotExpression, AndExpression, OrExpression
from .system import System
