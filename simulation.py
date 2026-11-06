import math
from typing import Callable, List, Tuple

from rk4 import rk4_step


Vector3 = Tuple[float, float, float]
State = Tuple[Vector3, Vector3]


def validate_vector(vector, name):
    if len(vector) != 3:
        raise ValueError(f"{name} must have exactly 3 components")

    values = tuple(float(x) for x in vector)

    if not all(math.isfinite(x) for x in values):
        raise ValueError(f"{name} contains invalid values")

    return values


def simulate_orbit(
    initial_position: Vector3,
    initial_velocity: Vector3,
    acceleration_function: Callable,
    duration: float,
    dt: float
) -> List[Tuple[float, Vector3, Vector3]]:

    duration = float(duration)
    dt = float(dt)

    if not math.isfinite(duration) or duration < 0:
        raise ValueError("Duration must be finite and non-negative")

    if not math.isfinite(dt) or dt <= 0:
        raise ValueError("Time step must be finite and positive")

    if not callable(acceleration_function):
        raise TypeError("Acceleration function must be callable")

    position = validate_vector(initial_position, "Initial position")
    velocity = validate_vector(initial_velocity, "Initial velocity")

    state: State = (position, velocity)

    results = [(0.0, position, velocity)]

    current_time = 0.0
    max_steps = 1_000_000
    step_count = 0

    while current_time < duration:

        if step_count >= max_steps:
            raise RuntimeError("Maximum simulation steps exceeded")

        step = min(dt, duration - current_time)

        state = rk4_step(
            state,
            step,
            acceleration_function
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


def calculate_distance(position: Vector3) -> float:
    x, y, z = position

    return math.sqrt(x*x + y*y + z*z)
