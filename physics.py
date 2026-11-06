import math
from typing import Tuple, Sequence

from bodies import G, CelestialBody

Vector3 = Tuple[float, float, float]


def vector_subtract(a: Vector3, b: Vector3) -> Vector3:
    return (
        a[0] - b[0],
        a[1] - b[1],
        a[2] - b[2]
    )


def calculate_distance(vector: Vector3) -> float:
    return math.sqrt(
        vector[0] ** 2 +
        vector[1] ** 2 +
        vector[2] ** 2
    )


def gravitational_acceleration(
    asteroid_position: Vector3,
    bodies: Sequence[CelestialBody]
) -> Vector3:

    ax = 0.0
    ay = 0.0
    az = 0.0

    for body in bodies:

        displacement = vector_subtract(
            body.position_m,
            asteroid_position
        )

        distance = calculate_distance(displacement)

        if distance == 0:
            raise ValueError(
                f"Asteroid position coincides with {body.name}"
            )

        factor = G * body.mass_kg / distance ** 3

        ax += factor * displacement[0]
        ay += factor * displacement[1]
        az += factor * displacement[2]

    acceleration = (ax, ay, az)

    if not all(math.isfinite(v) for v in acceleration):
        raise ArithmeticError("Invalid gravitational acceleration")

    return acceleration
