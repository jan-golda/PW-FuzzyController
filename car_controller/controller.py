import fuzzy_logic as fl

# default membership functions
DEFAULT_MEMBERSHIPS = {
  "car_speed": {
    "low": [(0, 1.0), (10.0, 1.0), (13.0, 0.0)],
    "target": [(10.0, 0.0), (13.0, 1.0), (16.0, 0.0)],
    "high": [(13.0, 0.0), (16.0, 1.0), (40.0, 1.0)]
  },
  "obstacle_distance": {
    "near": [(0.0, 1.0), (25.0, 1.0), (35.0, 0.0)],
    "target": [(25.0, 0.0), (35.0, 1.0), (45.0, 0.0)],
    "far": [(35.0, 0.0), (45.0, 1.0), (200.0, 1.0)]
  },
  "obstacle_relative_speed": {
    "approaching": [(-40.0, 1.0), (-20.0, 1.0), (-0.0, 0.0)],
    "constant": [(-20.0, 0.0), (0.0, 1.0), (20.0, 0.0)],
    "moving_away": [(0.0, 0.0), (20.0, 1.0), (40.0, 1.0)]
  },
  "car_acceleration": {
    "break_hard": [(-30.0, 1.0), (-20.0, 1.0), (-10.0, 0.0)],
    "break": [(-20.0, 0.0), (-10.0, 1.0), (-5.0, 1.0), (0.0, 0.0)],
    "maintain": [(-5.0, 0.0), (0.0, 1.0), (5.0, 0.0)],
    "accelerate": [(0.0, 0.0), (5.0, 1.0), (10.0, 1.0), (20.0, 0.0)],
    "accelerate_hard": [(10.0, 0.0), (20.0, 1.0), (30.0, 1.0)]
  }
}


class CarController:
    """ Implements the logic of a controller that controls vehicle acceleration. """

    def __init__(self, membership_points=DEFAULT_MEMBERSHIPS):
        """ Sets up the fuzzy logic system. """

        # car speed turned out to e redundant - the final system does not use it
        car_slow = fl.Term('car_speed', 'low', fl.PiecewiseMembership(membership_points['car_speed']['low']))
        car_target = fl.Term('car_speed', 'target', fl.PiecewiseMembership(membership_points['car_speed']['target']))
        car_fast = fl.Term('car_speed', 'high', fl.PiecewiseMembership(membership_points['car_speed']['high']))

        obstacle_near = fl.Term('obstacle_distance', 'near', fl.PiecewiseMembership(membership_points['obstacle_distance']['near']))
        obstacle_target = fl.Term('obstacle_distance', 'target', fl.PiecewiseMembership(membership_points['obstacle_distance']['target']))
        obstacle_far = fl.Term('obstacle_distance', 'far', fl.PiecewiseMembership(membership_points['obstacle_distance']['far']))

        obstacle_approaching = fl.Term('obstacle_relative_speed', 'approaching', fl.PiecewiseMembership(membership_points['obstacle_relative_speed']['approaching']))
        obstacle_static = fl.Term('obstacle_relative_speed', 'constant', fl.PiecewiseMembership(membership_points['obstacle_relative_speed']['constant']))
        obstacle_moving_away = fl.Term('obstacle_relative_speed', 'moving_away', fl.PiecewiseMembership(membership_points['obstacle_relative_speed']['moving_away']))

        car_break_hard = fl.Term('car_acceleration', 'break_hard', fl.PiecewiseMembership(membership_points['car_acceleration']['break_hard']))
        car_break = fl.Term('car_acceleration', 'break', fl.PiecewiseMembership(membership_points['car_acceleration']['break']))
        car_maintain = fl.Term('car_acceleration', 'maintain', fl.PiecewiseMembership(membership_points['car_acceleration']['maintain']))
        car_accelerate = fl.Term('car_acceleration', 'accelerate', fl.PiecewiseMembership(membership_points['car_acceleration']['accelerate']))
        car_accelerate_hard = fl.Term('car_acceleration', 'accelerate_hard', fl.PiecewiseMembership(membership_points['car_acceleration']['accelerate_hard']))

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
