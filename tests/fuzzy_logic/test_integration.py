import pytest

import fuzzy_logic as fl


def test_task_credit():
    """ Tests complete fuzzy logic system based on a example by Włodzimierz Kasprzak. """

    inputs = dict(
        przychod=3500,
        inwestycja=250000,
        wklad=35
    )

    przychod_maly = fl.Term('przychod', 'maly', fl.TrapezoidalMembership(None, 0, 1000, 3000))
    przychod_sredni = fl.Term('przychod', 'sredni', fl.TrapezoidalMembership(1000, 3000, 3500, 5000))
    przychod_duzy = fl.Term('przychod', 'duzy', fl.TrapezoidalMembership(3250, 5000, 10000, None))

    assert przychod_maly(**inputs) == 0
    assert przychod_sredni(**inputs) == 1
    assert przychod_duzy(**inputs) == 1/7

    inwestycja_maly = fl.Term('inwestycja', 'maly', fl.TrapezoidalMembership(None, 0, 200000, 400000))
    inwestycja_sredni = fl.Term('inwestycja', 'sredni', fl.TrapezoidalMembership(200000, 400000, 500000, 700000))
    inwestycja_duzy = fl.Term('inwestycja', 'duzy', fl.TrapezoidalMembership(450000, 700000, 1000000, None))

    assert inwestycja_maly(**inputs) == 3/4
    assert inwestycja_sredni(**inputs) == 1/4
    assert inwestycja_duzy(**inputs) == 0

    wklad_maly = fl.Term('wklad', 'maly', fl.TrapezoidalMembership(None, 0, 10, 25))
    wklad_sredni = fl.Term('wklad', 'sredni', fl.TrapezoidalMembership(10, 25, 35, 50))
    wklad_duzy = fl.Term('wklad', 'duzy', fl.TrapezoidalMembership(30, 50, 100, None))

    assert wklad_maly(**inputs) == 0
    assert wklad_sredni(**inputs) == 1
    assert wklad_duzy(**inputs) == 1/4

    kredyt_maly = fl.Term('kredyt', 'maly', fl.TrapezoidalMembership(None, 0, 20000, 200000))
    kredyt_sredni = fl.Term('kredyt', 'sredni', fl.TrapezoidalMembership(20000, 200000, 300000, 450000))
    kredyt_duzy = fl.Term('kredyt', 'duzy', fl.TrapezoidalMembership(250000, 450000, 1000000, None))

    rule1 = ((przychod_sredni & inwestycja_maly) | (inwestycja_sredni & wklad_maly)) >> kredyt_maly
    rule2 = ((przychod_sredni & inwestycja_sredni) | (przychod_maly & wklad_sredni)) >> kredyt_sredni
    rule3 = ((przychod_duzy & wklad_sredni) | (inwestycja_sredni & wklad_duzy)) >> kredyt_duzy

    assert rule1.antecedent(**inputs) == 3/4
    assert rule2.antecedent(**inputs) == 1/4
    assert rule3.antecedent(**inputs) == 1/4

    system = fl.System(rule1, rule2, rule3)

    assert system(**inputs)['kredyt'] == pytest.approx(420187.4163)
