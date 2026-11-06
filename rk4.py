from typing import Callable, Tuple

Vector3 = Tuple[float, float, float]
State = Tuple[Vector3, Vector3]


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(vector, factor):
    return tuple(x * factor for x in vector)


def add_states(a: State, b: State) -> State:
    return (
        add(a[0], b[0]),
        add(a[1], b[1])
    )


def scale_state(state: State, factor: float) -> State:
    return (
        scale(state[0], factor),
        scale(state[1], factor)
    )


def derivative(
    time: float,
    state: State,
    acceleration: Callable
) -> State:

    position, velocity = state

    return (
        velocity,
        acceleration(time, position)
    )


def rk4_step(
    time: float,
    state: State,
    dt: float,
    acceleration: Callable
) -> State:

    k1 = derivative(time, state, acceleration)

    k2_state = add_states(
        state,
        scale_state(k1, dt / 2)
    )
    k2 = derivative(time + dt / 2, k2_state, acceleration)

    k3_state = add_states(
        state,
        scale_state(k2, dt / 2)
    )
    k3 = derivative(time + dt / 2, k3_state, acceleration)

    k4_state = add_states(
        state,
        scale_state(k3, dt)
    )
    k4 = derivative(time + dt, k4_state, acceleration)

    weighted = add_states(
        add_states(k1, scale_state(k2, 2)),
        add_states(scale_state(k3, 2), k4)
    )

    return add_states(
        state,
        scale_state(weighted, dt / 6)
    )
