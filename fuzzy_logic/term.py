from fuzzy_logic import Membership, Expression


class Term(Expression):
    """ Represents a fuzzy term defined for a given membership function. """

    def __init__(self, variable: str, membership: Membership):
        self._variable = variable
        self._membership = membership

    def __call__(self, **inputs: float) -> float:
        return self._membership(inputs[self._variable])
