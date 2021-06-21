""" Unit tests of the expression system. """
import pytest as pytest

import fuzzy_logic as fl


@pytest.mark.parametrize('a', [0.0, 0.4, 1.0])
def test_not(a):
    term_a = fl.Term('a', 'A', fl.TriangularMembership(0, 1, 2))

    exp = ~term_a

    val_a = term_a(a=a)
    val_exp = exp(a=a)

    assert isinstance(exp, fl.NotExpression)
    assert val_exp == 1 - val_a


@pytest.mark.parametrize('a', [0.0, 0.4, 1.0])
@pytest.mark.parametrize('b', [0.0, 0.4, 1.0])
def test_or(a, b):
    term_a = fl.Term('a', 'A', fl.TriangularMembership(0, 1, 2))
    term_b = fl.Term('b', 'B', fl.TriangularMembership(0, 1, 2))

    exp = term_a | term_b

    val_exp = exp(a=a, b=b)
    val_a = term_a(a=a, b=b)
    val_b = term_b(a=a, b=b)

    assert isinstance(exp, fl.OrExpression)
    assert val_exp == max(val_a, val_b)


@pytest.mark.parametrize('a', [0.0, 0.4, 1.0])
@pytest.mark.parametrize('b', [0.0, 0.4, 1.0])
def test_and(a, b):
    term_a = fl.Term('a', 'A', fl.TriangularMembership(0, 1, 2))
    term_b = fl.Term('b', 'B', fl.TriangularMembership(0, 1, 2))

    exp = term_a & term_b

    val_exp = exp(a=a, b=b)
    val_a = term_a(a=a, b=b)
    val_b = term_b(a=a, b=b)

    assert isinstance(exp, fl.AndExpression)
    assert val_exp == min(val_a, val_b)


@pytest.mark.parametrize('a', [0.0, 0.4, 1.0])
@pytest.mark.parametrize('b', [0.0, 0.4, 1.0])
def test_complex(a, b):
    term_a = fl.Term('a', 'A', fl.TriangularMembership(0, 1, 2))
    term_b = fl.Term('b', 'B', fl.TriangularMembership(0, 1, 2))

    exp = (term_a & term_b) | ~term_a

    val_exp = exp(a=a, b=b)
    val_a = term_a(a=a, b=b)
    val_b = term_b(a=a, b=b)

    assert isinstance(exp, fl.OrExpression)
    assert isinstance(exp._left, fl.AndExpression)
    assert isinstance(exp._right, fl.NotExpression)
    assert val_exp == max(min(val_a, val_b), 1 - val_a)


def test_implication():
    term_a = fl.Term('a', 'A', fl.TriangularMembership(0, 1, 2))
    term_b = fl.Term('b', 'B', fl.TriangularMembership(0, 1, 2))

    impl = term_a >> term_b

    assert isinstance(impl, fl.Rule)
    assert impl == (term_a, term_b)
