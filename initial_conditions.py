import math
from typing import Tuple

Vector3 = Tuple[float, float, float]


def validate_vector(vector, name):
    if len(vector) != 3:
        raise ValueError(f"{name} must contain 3 values")

    result = tuple(float(value) for value in vector)

    if not all(math.isfinite(value) for value in result):
        raise ValueError(f"{name} must contain finite values")

    return result


def create_initial_conditions(position, velocity):
    position = validate_vector(position, "Position")
    velocity = validate_vector(velocity, "Velocity")

    if all(value == 0 for value in position):
        raise ValueError("Initial position cannot be zero")

    if all(value == 0 for value in velocity):
        raise ValueError("Initial velocity cannot be zero")

    return {
        "position_m": position,
        "velocity_m_s": velocity,
    }
