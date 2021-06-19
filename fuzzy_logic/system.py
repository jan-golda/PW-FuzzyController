import functools
import itertools
import operator
from typing import Iterable, Dict, List

import matplotlib
import matplotlib.pyplot as plt

from fuzzy_logic import Rule


def cleanup_rules(rules: Iterable[Rule]) -> Iterable[Rule]:
    """ Cleans up a set of rules by merging rules wih the same consequent. """
    for consequent, rules in itertools.groupby(rules, key=operator.attrgetter('consequent')):
        antecedent = map(operator.attrgetter('antecedent'), rules)
        antecedent = functools.reduce(operator.__or__, antecedent)
        yield antecedent >> consequent


def group_rules(rules: Iterable[Rule]) -> Dict[str, List[Rule]]:
    """ Groups rules by the variable of their consequent. """
    rules = sorted(rules, key=lambda r: r.consequent.variable)
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
        """ Evaluate this fuzzy logic system for the given inputs. """
        return {
            variable: evaluate_variable(rules, inputs)
            for variable, rules in self._rules.items()
        }

    def plot(self):
        """ Plot the membership graphs of this system. """
        inputs = set().union(*(r.antecedent.terms for r in itertools.chain.from_iterable(self._rules.values())))
        inputs = sorted(inputs, key=lambda t: t.variable)
        inputs = itertools.groupby(inputs, key=lambda t: t.variable)
        inputs = map(lambda t: ('input - '+t[0], list(t[1])), inputs)

        outputs = set(r.consequent for r in itertools.chain.from_iterable(self._rules.values()))
        outputs = sorted(outputs, key=lambda t: t.variable)
        outputs = itertools.groupby(outputs, key=lambda t: t.variable)
        outputs = map(lambda t: ('output - '+t[0], list(t[1])), outputs)

        variables = list(inputs) + list(outputs)

        fig, axs = plt.subplots(nrows=len(variables), figsize=(8, 2 * len(variables)))

        cmap = matplotlib.cm.get_cmap('tab10')
        for ax, (variable, terms) in zip(axs, variables):
            for i, term in enumerate(sorted(terms, key=lambda t: t.membership.center)):
                patch = term.plt_patch
                patch.set_alpha(0.4)
                patch.set_color(cmap(i))
                ax.add_patch(patch)

            ax.set_title(variable.replace('_', ' '))
            ax.set_yticks([])
            ax.legend(loc='upper right')
            ax.spines["top"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.autoscale()

        fig.tight_layout()
        plt.show()
