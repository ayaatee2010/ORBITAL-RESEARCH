import unittest
import math

from initial_conditions import create_initial_conditions
from uncertainty import generate_uncertainty_samples
from metrics import (
    position_error,
    velocity_error,
    calculate_rms,
    maximum_error,
)
from rk4 import rk4_step
from simulation import simulate_orbit


class TestOrbitalProject(unittest.TestCase):

    def test_initial_conditions(self):
        result = create_initial_conditions(
            (1.0, 0.0, 0.0),
            (0.0, 2.0, 0.0),
        )
        self.assertEqual(result["position_m"], (1.0, 0.0, 0.0))

    def test_invalid_initial_position(self):
        with self.assertRaises(ValueError):
            create_initial_conditions(
                (0.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
            )

    def test_uncertainty_sample_count(self):
        samples = generate_uncertainty_samples(
            (1e11, 0.0, 0.0),
            (0.0, 30000.0, 0.0),
            1000.0,
            1.0,
            sample_count=20,
        )
        self.assertEqual(len(samples), 20)

    def test_position_error(self):
        error = position_error(
            (3.0, 4.0, 0.0),
            (0.0, 0.0, 0.0),
        )
        self.assertAlmostEqual(error, 5.0)

    def test_velocity_error(self):
        error = velocity_error(
            (3.0, 4.0, 0.0),
            (0.0, 0.0, 0.0),
        )
        self.assertAlmostEqual(error, 5.0)

    def test_rms(self):
        self.assertAlmostEqual(
            calculate_rms([3.0, 4.0]),
            math.sqrt(12.5),
        )

    def test_maximum_error(self):
        self.assertEqual(maximum_error([2.0, 5.0, 3.0]), 5.0)

    def test_rk4_constant_velocity(self):
        def acceleration(time, position):
            return (0.0, 0.0, 0.0)

        state = (
            (0.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
        )

        result = rk4_step(0.0, state, 1.0, acceleration)

        self.assertAlmostEqual(result[0][0], 2.0)

    def test_simulation(self):
        def acceleration(time, position):
            return (0.0, 0.0, 0.0)

        result = simulate_orbit(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            acceleration,
            duration=2.0,
            dt=1.0,
        )

        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[-1][1][0], 2.0)


from physics import gravitational_acceleration
from bodies import CelestialBody


class TestGravity(unittest.TestCase):

    def test_sun_gravity_at_one_au(self):
        sun = CelestialBody("Sun", 1.98847e30)

        acceleration = gravitational_acceleration(
            (1.495978707e11, 0, 0),
            [sun],
            {"Sun": (0, 0, 0)}
        )

        self.assertLess(acceleration[0], 0)
        self.assertAlmostEqual(acceleration[1], 0)
        self.assertAlmostEqual(acceleration[2], 0)
        self.assertAlmostEqual(
            abs(acceleration[0]),
            0.00593,
            delta=0.00002
        )
if __name__ == "__main__":
    unittest.main()
