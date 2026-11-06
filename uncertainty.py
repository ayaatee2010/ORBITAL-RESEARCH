import math
import random

from initial_conditions import create_initial_conditions


def generate_uncertainty_samples(
    position,
    velocity,
    position_sigma,
    velocity_sigma,
    sample_count=100,
    seed=42,
):
    if not isinstance(sample_count, int) or sample_count < 1:
        raise ValueError("sample_count must be a positive integer")

    if position_sigma < 0 or velocity_sigma < 0:
        raise ValueError("Uncertainty values cannot be negative")

    if not math.isfinite(position_sigma):
        raise ValueError("Invalid position uncertainty")

    if not math.isfinite(velocity_sigma):
        raise ValueError("Invalid velocity uncertainty")

    initial = create_initial_conditions(position, velocity)
    rng = random.Random(seed)

    samples = []

    for index in range(sample_count):
        uncertain_position = tuple(
            value + rng.gauss(0, position_sigma)
            for value in initial["position_m"]
        )

        uncertain_velocity = tuple(
            value + rng.gauss(0, velocity_sigma)
            for value in initial["velocity_m_s"]
        )

        samples.append(
            create_initial_conditions(
                uncertain_position,
                uncertain_velocity,
            )
        )

    return samples
