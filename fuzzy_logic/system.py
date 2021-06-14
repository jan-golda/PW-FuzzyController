import functools
import itertools
import operator
from typing import Iterable, Dict, List

from fuzzy_logic import Rule


def cleanup_rules(rules: Iterable[Rule]) -> Iterable[Rule]:
    """ Cleans up a set of rules by merging rules wih the same consequent. """
    for consequent, rules in itertools.groupby(rules, key=operator.attrgetter('consequent')):
        antecedent = map(operator.attrgetter('antecedent'), rules)
        antecedent = functools.reduce(operator.__or__, antecedent)
        yield antecedent >> consequent


def group_rules(rules: Iterable[Rule]) -> Dict[str, List[Rule]]:
    """ Groups rules by the variable of their consequent. """
    groups = itertools.groupby(rules, key=lambda r: r.consequent.variable)
    groups = map(lambda g: (g[0], list(g[1])), groups)
    return dict(groups)


def evaluate_variable(rules: Iterable[Rule], inputs: Dict[str, float]) -> float:
    """ Evaluates a variable using the given inputs and rules (that all should be for this variable). """
    centers = [r.consequent.membership.center for r in rules]
    masses = [r.consequent.membership.mass for r in rules]
    values = [r.antecedent(**inputs) for r in rules]

    scaled_masses = [m * v for m, v in zip(masses, values)]
    weighted_centers = [c * m for c, m in zip(centers, scaled_masses)]

    return sum(weighted_centers) / sum(scaled_masses)


class System:
    """ Represents a fuzzy logic system that consists of rules. """

    def __init__(self, *rules: Rule):
        rules = cleanup_rules(rules)
        self._rules = group_rules(rules)

    def __call__(self, **inputs: float) -> Dict[str, float]:
        return {
            variable: evaluate_variable(rules, inputs)
            for variable, rules in self._rules.items()
        }
