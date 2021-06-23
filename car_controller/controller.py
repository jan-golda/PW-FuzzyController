import fuzzy_logic as fl


class CarController:
    """ Implements the logic of a controller that controls vehicle acceleration. """

    def __init__(self, distance_target: float = 35.0, distance_max: float = 200.0, distance_fuzzy: float = 10.0,
                 speed_target: float = 13.0, speed_fuzzy: float = 3.0, speed_max: float = 40.0,
                 acceleration_max: float = 30.0, deceleration_max: float = 30.0, acceleration_maintain_fuzzy: float = 5.0):
        """ Sets up the fuzzy logic system. """

        car_slow = fl.Term('car_speed', 'low', fl.TrapezoidalMembership(None, 0, speed_target - speed_fuzzy, speed_target))
        car_target = fl.Term('car_speed', 'target', fl.TriangularMembership(speed_target - speed_fuzzy, speed_target, speed_target + speed_fuzzy))
        car_fast = fl.Term('car_speed', 'high', fl.TrapezoidalMembership(speed_target, speed_target + speed_fuzzy, 40.0, None))

        obstacle_near = fl.Term('obstacle_distance', 'near', fl.TrapezoidalMembership(None, 0.0, distance_target - distance_fuzzy, distance_target))
        obstacle_target = fl.Term('obstacle_distance', 'target', fl.TriangularMembership(distance_target - distance_fuzzy, distance_target, distance_target + distance_fuzzy))
        obstacle_far = fl.Term('obstacle_distance', 'far', fl.TrapezoidalMembership(distance_target, distance_target + distance_fuzzy, distance_max, None))

        obstacle_approaching = fl.Term('obstacle_relative_speed', 'approaching', fl.TrapezoidalMembership(None, -speed_max, -speed_max / 2, -0.0))
        obstacle_static = fl.Term('obstacle_relative_speed', 'constant', fl.TriangularMembership(-speed_max / 2, 0.0, speed_max / 2))
        obstacle_moving_away = fl.Term('obstacle_relative_speed', 'moving_away', fl.TrapezoidalMembership(0.0, speed_max / 2, speed_max, None))

        car_break_hard = fl.Term('car_acceleration', 'break_hard', fl.TrapezoidalMembership(None, -deceleration_max, -deceleration_max * 2/3, -deceleration_max * 1/3))
        car_break = fl.Term('car_acceleration', 'break', fl.TrapezoidalMembership(-deceleration_max * 2/3, -deceleration_max * 1/3, -acceleration_maintain_fuzzy, 0.0))
        car_maintain = fl.Term('car_acceleration', 'maintain', fl.TriangularMembership(-acceleration_maintain_fuzzy, 0.0, acceleration_maintain_fuzzy))
        car_accelerate = fl.Term('car_acceleration', 'accelerate', fl.TrapezoidalMembership(0.0, acceleration_maintain_fuzzy, acceleration_max * 1/3, acceleration_max * 2/3))
        car_accelerate_hard = fl.Term('car_acceleration', 'accelerate_hard', fl.TrapezoidalMembership(acceleration_max * 1/3, acceleration_max * 2/3, acceleration_max, None))

        self._system = fl.System(
            obstacle_approaching >> car_break,
            obstacle_static >> car_maintain,
            obstacle_moving_away >> car_accelerate,
            obstacle_near >> car_break,
            obstacle_target >> car_maintain,
            obstacle_far >> car_accelerate,
            (obstacle_near & obstacle_approaching) >> car_break_hard
        )

    def __call__(self, car_speed: float, obstacle_distance: float, obstacle_relative_speed: float) -> float:
        """ Calculates the requested acceleration of a car based on the given variables. """
        return self._system(
            car_speed=car_speed,
            obstacle_distance=obstacle_distance,
            obstacle_relative_speed=obstacle_relative_speed
        )['car_acceleration']

    @property
    def system(self) -> fl.System:
        return self._system
