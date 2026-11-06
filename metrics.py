import math


def position_error(predicted, reference):
    if len(predicted) != 3 or len(reference) != 3:
        raise ValueError("Positions must have 3 components")

    return math.sqrt(
        sum(
            (float(p) - float(r)) ** 2
            for p, r in zip(predicted, reference)
        )
    )


def velocity_error(predicted, reference):
    if len(predicted) != 3 or len(reference) != 3:
        raise ValueError("Velocities must have 3 components")

    return math.sqrt(
        sum(
            (float(p) - float(r)) ** 2
            for p, r in zip(predicted, reference)
        )
    )


def calculate_rms(errors):
    if not errors:
        raise ValueError("At least one error is required")

    values = [float(error) for error in errors]

    if not all(math.isfinite(value) and value >= 0 for value in values):
        raise ValueError("Errors must be finite and non-negative")

    return math.sqrt(
        sum(value ** 2 for value in values) / len(values)
    )


def maximum_error(errors):
    if not errors:
        raise ValueError("At least one error is required")

    values = [float(error) for error in errors]

    if not all(math.isfinite(value) and value >= 0 for value in values):
        raise ValueError("Errors must be finite and non-negative")

    return max(values)
