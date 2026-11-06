import math
from typing import Callable, List, Tuple

from rk4 import rk4_step

Vector3 = Tuple[float, float, float]
State = Tuple[Vector3, Vector3]
TrajectoryPoint = Tuple[float, Vector3, Vector3]


def validate_vector(vector, name):
    if len(vector) != 3:
        raise ValueError(f"{name} must have 3 components")

    result = tuple(float(x) for x in vector)

    if not all(math.isfinite(x) for x in result):
        raise ValueError(f"{name} contains invalid values")

    return result


def simulate_orbit(
    initial_position: Vector3,
    initial_velocity: Vector3,
    acceleration: Callable,
    duration: float,
    dt: float
) -> List[TrajectoryPoint]:

    duration = float(duration)
    dt = float(dt)

    if not math.isfinite(duration) or duration < 0:
        raise ValueError("Duration must be non-negative")

    if not math.isfinite(dt) or dt <= 0:
        raise ValueError("Time step must be positive")

    if not callable(acceleration):
        raise TypeError("Acceleration must be callable")

    position = validate_vector(initial_position, "Position")
    velocity = validate_vector(initial_velocity, "Velocity")

    state: State = (position, velocity)

    results = [(0.0, position, velocity)]

    current_time = 0.0
    step_count = 0
    max_steps = 1_000_000

    while current_time < duration:

        if step_count >= max_steps:
            raise RuntimeError("Maximum steps exceeded")

        step = min(dt, duration - current_time)

        state = rk4_step(
            current_time,
            state,
            step,
            acceleration
        )

        position, velocity = state

        position = validate_vector(position, "Position")
        velocity = validate_vector(velocity, "Velocity")

        current_time += step
        step_count += 1

        results.append(
            (current_time, position, velocity)
        )

    return results


def calculate_distance(position):
    return math.sqrt(sum(x * x for x in position))
