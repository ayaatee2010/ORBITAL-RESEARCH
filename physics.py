import math
from typing import Mapping, Sequence

from bodies import G, CelestialBody

Vector3 = tuple[float, float, float]


def validate_vector(vector, name):
    if len(vector) != 3:
        raise ValueError(f"{name} must have 3 components")

    result = tuple(float(x) for x in vector)

    if not all(math.isfinite(x) for x in result):
        raise ValueError(f"{name} contains invalid values")

    return result


def vector_subtract(a: Vector3, b: Vector3) -> Vector3:
    return tuple(x - y for x, y in zip(a, b))


def calculate_distance(vector: Vector3) -> float:
    return math.sqrt(sum(x * x for x in vector))


def gravitational_acceleration(
    asteroid_position: Vector3,
    bodies: Sequence[CelestialBody],
    body_positions: Mapping[str, Vector3],
) -> Vector3:

    asteroid_position = validate_vector(
        asteroid_position, "Asteroid position"
    )

    ax = ay = az = 0.0

    for body in bodies:
        if body.name not in body_positions:
            raise ValueError(
                f"Missing position for {body.name}"
            )

        body_position = validate_vector(
            body_positions[body.name],
            f"{body.name} position",
        )

        displacement = vector_subtract(
            body_position,
            asteroid_position,
        )

        distance = calculate_distance(displacement)

        if distance == 0:
            raise ValueError(
                f"Asteroid coincides with {body.name}"
            )

        factor = G * body.mass_kg / distance**3

        ax += factor * displacement[0]
        ay += factor * displacement[1]
        az += factor * displacement[2]

    result = (ax, ay, az)

    if not all(math.isfinite(x) for x in result):
        raise ArithmeticError("Non-finite acceleration")

    return result


def make_acceleration_function(bodies, body_provider):

    def acceleration(time, asteroid_position):
        positions = body_provider(time)

        return gravitational_acceleration(
            asteroid_position,
            bodies,
            positions,
        )

    return acceleration
