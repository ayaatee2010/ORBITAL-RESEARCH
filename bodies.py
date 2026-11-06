from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CelestialBody:
    name: str
    mass_kg: float
    position_m: Tuple[float, float, float]


# Gravitational constant (SI)
G = 6.67430e-11


# Solar system reference masses (kg)
BODIES = {
    "Sun": CelestialBody(
        "Sun",
        1.98847e30,
        (0.0, 0.0, 0.0)
    ),

    "Mercury": CelestialBody(
        "Mercury",
        3.3011e23,
        (0.0, 0.0, 0.0)
    ),

    "Venus": CelestialBody(
        "Venus",
        4.8675e24,
        (0.0, 0.0, 0.0)
    ),

    "Earth": CelestialBody(
        "Earth",
        5.97237e24,
        (0.0, 0.0, 0.0)
    ),

    "Mars": CelestialBody(
        "Mars",
        6.4171e23,
        (0.0, 0.0, 0.0)
    ),

    "Jupiter": CelestialBody(
        "Jupiter",
        1.8982e27,
        (0.0, 0.0, 0.0)
    ),

    "Saturn": CelestialBody(
        "Saturn",
        5.6834e26,
        (0.0, 0.0, 0.0)
    ),

    "Uranus": CelestialBody(
        "Uranus",
        8.6810e25,
        (0.0, 0.0, 0.0)
    ),

    "Neptune": CelestialBody(
        "Neptune",
        1.02413e26,
        (0.0, 0.0, 0.0)
    )
}


def get_body(name: str) -> CelestialBody:
    try:
        return BODIES[name]
    except KeyError:
        raise ValueError(f"Unknown celestial body: {name}")


def list_bodies():
    return tuple(BODIES.keys())
