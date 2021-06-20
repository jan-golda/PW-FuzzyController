from unittest.mock import Mock

import pytest

from car_controller import CarSimulation
from fuzzy_logic import System


def pytest_addoption(parser):
    parser.addoption("--plot", action='store_true', help="display plots of the simulation")


@pytest.fixture(autouse=True)
def disable_plotting(pytestconfig, monkeypatch):
    if not pytestconfig.getoption('plot'):
        monkeypatch.setattr(System, 'plot', Mock())
        monkeypatch.setattr(CarSimulation, 'plot', Mock())
