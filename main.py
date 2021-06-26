""" CLI entrypoint for the application. """
import argparse
import csv
import json
import sys

from car_controller import CarController, CarSimulation


def parse_arguments():
    """ Parses provided command line arguments. """
    parser = argparse.ArgumentParser(description='Fuzzy logic driven car acceleration controller')
    parser.add_argument('-m', '--memberships', metavar='FILE', type=argparse.FileType('r'), help='optional JSON file with the definitions of the memberships')
    parser.add_argument('-o', '--output', metavar='FILE', type=argparse.FileType('w'), help='write the simulation logs to a file')
    parser.add_argument('-ps', '--plot-simulation', action='store_true', help='[requires matplotlib] show a plot of the simulation results')
    parser.add_argument('-pm', '--plot-membership', action='store_true', help='[requires matplotlib] show a plot of the membership functions')

    scenario_subparsers = parser.add_subparsers(dest='scenario', title='Available scenarios', help='scenario for which to run the simulation')

    parser_manual = scenario_subparsers.add_parser('manual', help='runs the controller in a manual mode in which the user can directly experiment with it')

    parser_stationary = scenario_subparsers.add_parser('stationary', help='scenario in which the obstacle is stationary')
    parser_stationary.add_argument('-st', '--simulation-time', required=True, type=float, help='duration of the simulation')
    parser_stationary.add_argument('-ts', '--time-step', default=0.05, type=float, help='time step of the simulation')
    parser_stationary.add_argument('-cs', '--car-speed', required=True, type=float, help='initial speed of the car')
    parser_stationary.add_argument('-op', '--obstacle-position', required=True, type=float, help='initial position of the obstacle')

    parser_constant = scenario_subparsers.add_parser('constant', help='scenario in which the obstacle moves at a constant speed')
    parser_constant.add_argument('-st', '--simulation-time', required=True, type=float, help='duration of the simulation')
    parser_constant.add_argument('-ts', '--time-step', default=0.05, type=float, help='time step of the simulation')
    parser_constant.add_argument('-cs', '--car-speed', required=True, type=float, help='initial speed of the car')
    parser_constant.add_argument('-os', '--obstacle-speed', required=True, type=float, help='constant speed of the obstacle')
    parser_constant.add_argument('-op', '--obstacle-position', required=True, type=float, help='initial position of the obstacle')

    parser_acceleration = scenario_subparsers.add_parser('acceleration', help='scenario in which the obstacle accelerates/decelerates form one speed to another')
    parser_acceleration.add_argument('-ts', '--time-step', default=0.05, type=float, help='time step of the simulation')
    parser_acceleration.add_argument('-cs', '--car-speed', required=True, type=float, help='initial speed of the car')
    parser_acceleration.add_argument('-os', '--obstacle-initial-speed', required=True, type=float, help='initial speed of the obstacle')
    parser_acceleration.add_argument('-ot', '--obstacle-target-speed', required=True, type=float, help='target speed of the obstacle')
    parser_acceleration.add_argument('-oa', '--obstacle-acceleration', required=True, type=float, help='acceleration (absolute) of the obstacle')
    parser_acceleration.add_argument('-op', '--obstacle-position', required=True, type=float, help='initial position of the obstacle')

    return parser.parse_args()


def create_controller(args: argparse.Namespace):
    """ Configures the car controller based on the arguments. """
    if args.memberships:
        return CarController(membership_points=json.load(args.memberships))
    return CarController()


def run_manually(car_controller: CarController):
    """ Runs the controller in a manual mode in which the user can directly experiment with it. """
    while True:
        try:
            print()
            car_speed = float(input('Enter car speed [m/s, float]: '))
            obstacle_distance = float(input('Enter distance from obstacle [m, float]: '))
            obstacle_relative_speed = float(input('Enter relative speed of car and obstacle [m/s, float]: '))

            acceleration = car_controller(
                car_speed=car_speed,
                obstacle_distance=obstacle_distance,
                obstacle_relative_speed=obstacle_relative_speed
            )

            print('Calculated acceleration [m/s^2]:', acceleration)
        except KeyboardInterrupt:
            print('\nTerminated')
            return
        except Exception as e:
            print('An error occurred:', e)


def main():
    """ Main entrypoint. """
    args = parse_arguments()

    # setup controller
    controller = create_controller(args)

    # manual mode needs only the controller
    if args.scenario == 'manual':
        run_manually(controller)
        sys.exit()

    # setup a simulation scenario
    if args.scenario == 'stationary':
        simulation = CarSimulation(
            initial_car_position=0.0,
            initial_car_speed=args.car_speed,
            initial_obstacle_position=args.obstacle_position,
            initial_obstacle_speed=0.0
        )
        simulation_time = args.simulation_time
        obstacle_acceleration = 0.0

    if args.scenario == 'constant':
        simulation = CarSimulation(
            initial_car_position=0.0,
            initial_car_speed=args.car_speed,
            initial_obstacle_position=args.obstacle_position,
            initial_obstacle_speed=args.obstacle_speed
        )
        simulation_time = args.simulation_time
        obstacle_acceleration = 0.0

    if args.scenario == 'acceleration':
        simulation = CarSimulation(
            initial_car_position=0.0,
            initial_car_speed=args.car_speed,
            initial_obstacle_position=args.obstacle_position,
            initial_obstacle_speed=args.obstacle_initial_speed
        )
        simulation_time = abs(args.obstacle_target_speed - args.obstacle_initial_speed) / args.obstacle_acceleration + 4.0
        obstacle_acceleration = lambda t: (
            (args.obstacle_acceleration if args.obstacle_target_speed > args.obstacle_initial_speed else -args.obstacle_acceleration)
            if 2.0 <= t < 2.0 + abs(args.obstacle_target_speed - args.obstacle_initial_speed) / args.obstacle_acceleration else
            0.0
        )

    # run the simulation
    simulation.simulate(
        car_controller=controller,
        obstacle_acceleration=obstacle_acceleration,
        simulation_time=simulation_time
    )

    # plotting (if requested)
    if args.plot_membership:
        controller.system.plot()
    if args.plot_simulation:
        simulation.plot()

    # get the simulation history
    data = list(simulation)
    headers = list(data[0].keys())

    # print the simulation results
    for step in data:
        for header in headers:
            print(f'{header}={step[header]:.3f}  ', end='')
        print()

    # save the simulation results to file
    if args.output:
        writer = csv.DictWriter(args.output, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


if __name__ == '__main__':
    main()
