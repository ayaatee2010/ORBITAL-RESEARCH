import math

def gravitational_acceleration(position, sun_mass):
    G = 6.67430e-11

    x, y, z = position

    r = math.sqrt(x*x + y*y + z*z)

    if r == 0:
        raise ValueError("Position cannot be zero")

    factor = -G * sun_mass / (r**3)

    return (
        factor * x,
        factor * y,
        factor * z
    )


if __name__ == "__main__":
    SUN_MASS = 1.98847e30

    position = (1.496e11, 0, 0)

    acceleration = gravitational_acceleration(
        position,
        SUN_MASS
    )

    print("ORBITAL — First gravitational calculation")
    print("Acceleration (m/s²):", acceleration)
