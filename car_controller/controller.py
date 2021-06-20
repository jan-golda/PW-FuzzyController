import fuzzy_logic as fl


class CarController:
    """ Implements the logic of a controlelr that controlle vehicle acceleration. """

    def __init__(self):

        speed_low = fl.Term('car_speed', 'low', fl.TrapezoidalMembership(None, 0, 10.0, 12.0))
        speed_target = fl.Term('car_speed', 'target', fl.TrapezoidalMembership(10.0, 12.0, 14.0, 16.0))
        speed_high = fl.Term('car_speed', 'high', fl.TrapezoidalMembership(14.0, 16.0, 40.0, None))

        obstacle_near = fl.Term('obstacle_distance', 'near', fl.TrapezoidalMembership(None, 0.0, 20.0, 30.0))
        obstacle_target = fl.Term('obstacle_distance', 'target', fl.TrapezoidalMembership(20.0, 30.0, 40.0, 50.0))
        obstacle_far = fl.Term('obstacle_distance', 'far', fl.TrapezoidalMembership(40.0, 50.0, 200.0, None))

        obstacle_approaching = fl.Term('obstacle_relative_speed', 'approaching', fl.TrapezoidalMembership(None, -40.0, -4.0, -2.0))
        obstacle_static = fl.Term('obstacle_relative_speed', 'constant', fl.TrapezoidalMembership(-4.0, -2.0, 2.0, 4.0))
        obstacle_moving_away = fl.Term('obstacle_relative_speed', 'moving_away', fl.TrapezoidalMembership(2.0, 4.0, 40.0, None))

        car_break_hard = fl.Term('car_acceleration', 'break_hard', fl.TrapezoidalMembership(None, -30.0, -20.0, -10.0))
        car_break = fl.Term('car_acceleration', 'break', fl.TrapezoidalMembership(-20.0, -10.0, -5.0, -2.0))
        car_maintain = fl.Term('car_acceleration', 'maintain', fl.TrapezoidalMembership(-5.0, -2.0, 2.0, 5.0))
        car_accelerate = fl.Term('car_acceleration', 'accelerate', fl.TrapezoidalMembership(2.0, 5.0, 10.0, 20.0))
        car_accelerate_hard = fl.Term('car_acceleration', 'accelerate_hard', fl.TrapezoidalMembership(10.0, 20.0, 30.0, None))

        self._system = fl.System(
            (speed_low & ~obstacle_near) >> car_accelerate,
            speed_target >> car_maintain,
            speed_high >> car_break,
            obstacle_near >> car_break,
            (obstacle_near & obstacle_approaching) >> car_break_hard
        )

    def __call__(self, car_speed: float, obstacle_distance: float, obstacle_relative_speed: float) -> float:
        return self._system(
            car_speed=car_speed,
            obstacle_distance=obstacle_distance,
            obstacle_relative_speed=obstacle_relative_speed
        )['car_acceleration']

    @property
    def system(self) -> fl.System:
        return self._system