from typing import Union, Callable, Tuple

import matplotlib.pyplot as plt

from car_controller import CarController


class CarSimulation:

    def __init__(self,
                 initial_car_position: float = 0.0,
                 initial_car_speed: float = 0.0,
                 initial_obstacle_position: float = 10.0,
                 initial_obstacle_speed: float = 1.0):
        """ Initializes the simulation. """
        self._car_positions = [initial_car_position]
        self._car_speeds = [initial_car_speed]
        self._car_accelerations = [0.0]

        self._obstacle_positions = [initial_obstacle_position]
        self._obstacle_speeds = [initial_obstacle_speed]
        self._obstacle_accelerations = [0.0]

        self._simulation_times = [0.0]

    def step(self, time_step: float = 0.1):
        """ Performs one step of the simulation. """
        self._simulation_times.append(self.current_simulation_time + time_step)

        self._car_speeds.append(max(0.0, self.current_car_speed + self.current_car_acceleration * time_step))
        self._car_positions.append(self.current_car_position + sum(self._car_speeds[-2:]) / 2 * time_step)
        self._car_accelerations.append(self.current_car_acceleration)

        self._obstacle_speeds.append(max(0.0, self.current_obstacle_speed + self.current_obstacle_acceleration * time_step))
        self._obstacle_positions.append(self.current_obstacle_position + sum(self._obstacle_speeds[-2:]) / 2 * time_step)
        self._obstacle_accelerations.append(self.current_obstacle_acceleration)

    def simulate(self, car_controller: CarController, obstacle_acceleration: Union[float, Callable[[float], float]], simulation_time: float, time_step: float = 0.05):
        """ Runs the simulation for a given number of steps using the given controller. """
        # turn a constant value into a constant function
        if not callable(obstacle_acceleration):
            obstacle_acceleration_value = obstacle_acceleration
            obstacle_acceleration = lambda t: obstacle_acceleration_value

        # rune the simulation
        for i in range(int(simulation_time / time_step)):
            self.current_car_acceleration = car_controller(
                car_speed=self.current_car_speed,
                obstacle_distance=self.current_obstacle_position - self.current_car_position,
                obstacle_relative_speed=self.current_obstacle_speed - self.current_car_speed
            )
            self.current_obstacle_acceleration = obstacle_acceleration(self.current_simulation_time)
            self.step(time_step)

    def plot(self, title: str = '', accelerations_limits: Tuple[float, float] = (-30, 30), speed_limits: Tuple[float, float] = (-1, 40)):
        fig, axs = plt.subplots(nrows=3)

        axs[0].set_ylabel(r'position $\left[m\right]$')
        axs[0].plot(self._simulation_times, self._car_positions, label='car')
        axs[0].plot(self._simulation_times, self._obstacle_positions, label='obstacle')

        axs[1].set_ylabel(r'speed $\left[\frac{m}{s}\right]$')
        axs[1].plot(self._simulation_times, self._car_speeds, label='car')
        axs[1].plot(self._simulation_times, self._obstacle_speeds, label='obstacle')
        axs[1].set_ylim(speed_limits)

        axs[2].set_ylabel(r'acceleration $\left[\frac{m}{s^2}\right]$')
        axs[2].step(self._simulation_times, self._car_accelerations, where='post', label='car')
        axs[2].step(self._simulation_times, self._obstacle_accelerations, where='post', label='obstacle')
        axs[2].set_ylim(accelerations_limits)

        axs[0].set_xticks([])
        axs[1].set_xticks([])
        axs[2].set_xlabel(r'time $\left[s\right]$')

        fig.legend(*axs[2].get_legend_handles_labels(), loc='upper center', ncol=2)
        fig.subplots_adjust(wspace=0, hspace=0.1)

        if title:
            axs[0].set_title(title)

        plt.show()

    @property
    def collision(self) -> bool:
        """ If at any point in this simulation the car and obstacle collided. """
        return any(op - cp <= 0 for cp, op in zip(self._car_positions, self._obstacle_positions))

    @property
    def current_car_position(self) -> float:
        return self._car_positions[-1]

    @property
    def current_car_speed(self) -> float:
        return self._car_speeds[-1]

    @property
    def current_car_acceleration(self) -> float:
        return self._car_accelerations[-1]

    @current_car_acceleration.setter
    def current_car_acceleration(self, value: float):
        self._car_accelerations[-1] = value

    @property
    def current_obstacle_position(self) -> float:
        return self._obstacle_positions[-1]

    @property
    def current_obstacle_speed(self) -> float:
        return self._obstacle_speeds[-1]

    @property
    def current_obstacle_acceleration(self) -> float:
        return self._obstacle_accelerations[-1]

    @current_obstacle_acceleration.setter
    def current_obstacle_acceleration(self, value: float):
        self._obstacle_accelerations[-1] = value

    @property
    def current_simulation_time(self):
        return self._simulation_times[-1]
