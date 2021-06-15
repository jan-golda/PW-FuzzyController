import fuzzy_logic as fl
from fuzzy_logic.system import cleanup_rules, group_rules


def test_cleanup_rules():
    term_a = fl.Term('a', 'A', fl.TriangularMembership(0, 1, 2))
    term_b = fl.Term('b', 'B', fl.TriangularMembership(0, 1, 2))

    rules = list(cleanup_rules([
        term_a >> term_b,
        term_b >> term_b,
        term_a >> term_a
    ]))

    assert len(rules) == 2
    assert isinstance(rules[0], fl.Rule)
    assert isinstance(rules[1], fl.Rule)
    assert isinstance(rules[0].antecedent, fl.OrExpression)
    assert rules[0].antecedent._left == term_a
    assert rules[0].antecedent._right == term_b
    assert rules[0].consequent == term_b
    assert rules[1].antecedent == term_a
    assert rules[1].consequent == term_a


def test_group_rules():
    term_a = fl.Term('a', 'A', fl.TriangularMembership(0, 1, 2))
    term_b = fl.Term('b', 'B', fl.TriangularMembership(0, 1, 2))

    groups = group_rules([
        term_a >> term_b,
        term_b >> term_b,
        term_a >> term_a
    ])

    assert len(groups) == 2
    assert len(groups['a']) == 1
    assert len(groups['b']) == 2
