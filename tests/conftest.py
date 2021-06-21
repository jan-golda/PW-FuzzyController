from unittest.mock import Mock

import pytest

from car_controller import CarSimulation
from fuzzy_logic import System


def pytest_addoption(parser):
    """ Adds a custom --plot flag to the pytest that enables plotting of the simulations in tests. """
    parser.addoption("--plot", action='store_true', help="display plots of the simulation")


@pytest.fixture(autouse=True)
def disable_plotting(pytestconfig, monkeypatch):
    """ Patches the plotting functions if --plot flag was not provided. """
    if not pytestconfig.getoption('plot'):
        monkeypatch.setattr(System, 'plot', Mock())
        monkeypatch.setattr(CarSimulation, 'plot', Mock())
