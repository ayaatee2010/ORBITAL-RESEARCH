from dataclasses import dataclass
import math


G = 6.67430e-11


@dataclass(frozen=True)
class CelestialBody:
    name: str
    mass_kg: float

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Body name cannot be empty")

        if not math.isfinite(self.mass_kg) or self.mass_kg <= 0:
            raise ValueError("Mass must be positive and finite")


BODIES = {
    "Sun": CelestialBody(
        "Sun", 1.98847e30
    ),
    "Mercury": CelestialBody(
        "Mercury", 3.3011e23
    ),
    "Venus": CelestialBody(
        "Venus", 4.8675e24
    ),
    "Earth": CelestialBody(
        "Earth", 5.97237e24
    ),
    "Mars": CelestialBody(
        "Mars", 6.4171e23
    ),
    "Jupiter": CelestialBody(
        "Jupiter", 1.8982e27
    ),
    "Saturn": CelestialBody(
        "Saturn", 5.6834e26
    ),
    "Uranus": CelestialBody(
        "Uranus", 8.6810e25
    ),
    "Neptune": CelestialBody(
        "Neptune", 1.02413e26
    ),
}


def get_body(name):
    if name not in BODIES:
        raise ValueError(f"Unknown celestial body: {name}")

    return BODIES[name]


def list_bodies():
    return list(BODIES.values())
