""" Tests of the car controller in different situations. """
import itertools

import pytest

from car_controller import CarController, CarSimulation


@pytest.mark.parametrize('initial_speed', [7.0, 14.0, 21.0, 28.0])
@pytest.mark.parametrize('deceleration', [10.0, 20.0, 30.0])
def test_obstacle_emergency_breaking(initial_speed, deceleration):
    """
    Tests a situation when both car and obstacle are moving at a constant speed
    with 35m between them and then the obstacle breaks to 0.
    """
    car_controller = CarController()
    simulation = CarSimulation(
        initial_car_speed=initial_speed,
        initial_obstacle_speed=initial_speed,
        initial_obstacle_position=35.0
    )
    obstacle_acceleration = lambda t: (
        -deceleration
        if 2.0 <= t < 2.0 + initial_speed / deceleration else
        0.0
    )

    simulation.simulate(car_controller, obstacle_acceleration, simulation_time=20.0)
    simulation.plot(title=f'Initial speed: {initial_speed}, Obstacle deceleration: {deceleration}')

    assert not simulation.collision
    assert simulation.current_car_speed == 0.0


@pytest.mark.parametrize('car_speed', [7.0, 14.0, 21.0, 28.0])
@pytest.mark.parametrize('obstacle_speed', [7.0, 14.0, 21.0, 28.0])
def test_obstacle_constant_speed(car_speed, obstacle_speed):
    """
    Tests the situation when a obstacle is moving at a constant speed and the
    car has to adapt to it.
    """
    car_controller = CarController()
    simulation = CarSimulation(
        initial_car_speed=car_speed,
        initial_obstacle_speed=obstacle_speed,
        initial_obstacle_position=35.0
    )
    obstacle_acceleration = 0.0

    simulation.simulate(car_controller, obstacle_acceleration, simulation_time=20.0)
    simulation.plot(title=f'Initial car speed: {car_speed}, Obstacle speed: {obstacle_speed}')

    assert not simulation.collision
    assert simulation.current_obstacle_position - simulation.current_car_position == pytest.approx(35.0, abs=1.0)


@pytest.mark.parametrize('initial_speed,target_speed', list(itertools.permutations([7.0, 14.0, 21.0, 28.0], 2)))
@pytest.mark.parametrize('acceleration', [2.5, 5.0, 10.0, 15.0])
def test_obstacle_speed_change(initial_speed, target_speed, acceleration):
    """
    Tests a situation when both car and obstacle are moving at a constant speed
    with 35m between them and then the obstacle speed changes.
    """
    car_controller = CarController()
    simulation = CarSimulation(
        initial_car_speed=initial_speed,
        initial_obstacle_speed=initial_speed,
        initial_obstacle_position=35.0
    )
    obstacle_acceleration = lambda t: (
        (acceleration if target_speed > initial_speed else -acceleration)
        if 2.0 <= t < 2.0 + abs(target_speed - initial_speed) / acceleration else
        0.0
    )

    simulation.simulate(car_controller, obstacle_acceleration, simulation_time=20.0)
    simulation.plot(title=f'Initial speed: {initial_speed}, Target speed: {target_speed}, Acceleration: {acceleration}')

    assert not simulation.collision
    assert simulation.current_obstacle_position - simulation.current_car_position == pytest.approx(35.0, abs=1.0)


@pytest.mark.parametrize('car_speed', [7.0, 14.0, 21.0, 28.0])
@pytest.mark.parametrize('obstacle_position', [35.0, 50.0, 100.0, 150.0, 200.0])
def test_obstacle_static(car_speed, obstacle_position):
    """
    Tests a situation when the obstacle stands still and the car needs to
    brake to stop.
    """
    car_controller = CarController()
    simulation = CarSimulation(
        initial_car_speed=car_speed,
        initial_obstacle_speed=0.0,
        initial_obstacle_position=obstacle_position
    )
    obstacle_acceleration = 0.0

    simulation.simulate(car_controller, obstacle_acceleration, simulation_time=20.0)
    simulation.plot(title=f'Initial car speed: {car_speed}, Obstacle position: {obstacle_position}')

    assert not simulation.collision


@pytest.mark.parametrize('target_speed', [7.0, 14.0, 21.0, 28.0])
@pytest.mark.parametrize('obstacle_position', [35.0, 50.0, 100.0])
@pytest.mark.parametrize('acceleration', [2.5, 5.0, 10.0, 15.0])
def test_obstacle_start(target_speed, obstacle_position, acceleration):
    """
    Tests a situation when both car and obstacle are standing still and then the
    obstacle moves and the car needs to follow it.
    """
    car_controller = CarController()
    simulation = CarSimulation(
        initial_car_speed=0.0,
        initial_obstacle_speed=0.0,
        initial_obstacle_position=obstacle_position
    )
    obstacle_acceleration = lambda t: (
        acceleration
        if 2.0 <= t < 2.0 + target_speed / acceleration else
        0.0
    )

    simulation.simulate(car_controller, obstacle_acceleration, simulation_time=20.0)
    simulation.plot(title=f'Target speed: {target_speed}, Obstacle position: {obstacle_position}, Acceleration: {acceleration}')

    assert not simulation.collision
    assert simulation.current_car_speed == pytest.approx(target_speed, abs=1.0)


def test_traffic_jam():
    """
    Tests the situation when the car and obstacle are moving in a "traffic jam"
    which consists of frequent, small changes in the speed.
    """
    TIMES = [1, 3, 5, 6, 8, 10, 12, 14, 16, 20, 21, 22, 23, 25]
    ACCELERATIONS = [0.0, 2.0, 0.0, -4.0, 0.0, 4.0, 0.0, 2.0, -6.0, 0.0, 2.0, 0.0, 2.0, 0.0]

    def obstacle_acceleration(t):
        for time, acc in zip(TIMES, ACCELERATIONS):
            if time >= t:
                return acc

    car_controller = CarController()
    simulation = CarSimulation(
        initial_car_speed=0.0,
        initial_obstacle_speed=0.0,
        initial_obstacle_position=35.0
    )

    simulation.simulate(car_controller, obstacle_acceleration, simulation_time=25.0)
    simulation.plot()

    assert not simulation.collision
