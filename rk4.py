def add_vectors(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale_vector(vector, scalar):
    return tuple(scalar * x for x in vector)


def derivative(state, acceleration_function):
    position, velocity = state
    acceleration = acceleration_function(position)

    return velocity, acceleration


def rk4_step(state, dt, acceleration_function):
    def evaluate(current_state):
        return derivative(current_state, acceleration_function)

    k1 = evaluate(state)

    state2 = (
        add_vectors(state[0], scale_vector(k1[0], dt / 2)),
        add_vectors(state[1], scale_vector(k1[1], dt / 2))
    )
    k2 = evaluate(state2)

    state3 = (
        add_vectors(state[0], scale_vector(k2[0], dt / 2)),
        add_vectors(state[1], scale_vector(k2[1], dt / 2))
    )
    k3 = evaluate(state3)

    state4 = (
        add_vectors(state[0], scale_vector(k3[0], dt)),
        add_vectors(state[1], scale_vector(k3[1], dt))
    )
    k4 = evaluate(state4)

    position = add_vectors(
        state[0],
        scale_vector(
            add_vectors(
                add_vectors(k1[0], scale_vector(k2[0], 2)),
                add_vectors(scale_vector(k3[0], 2), k4[0])
            ),
            dt / 6
        )
    )

    velocity = add_vectors(
        state[1],
        scale_vector(
            add_vectors(
                add_vectors(k1[1], scale_vector(k2[1], 2)),
                add_vectors(scale_vector(k3[1], 2), k4[1])
            ),
            dt / 6
        )
    )

    return position, velocity
