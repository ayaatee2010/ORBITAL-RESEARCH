
import unittest
from ephemeris import interpolate_state


class TestEphemeris(unittest.TestCase):

    def setUp(self):
        # One day = 86400 seconds.
        # Constant velocity gives an exact linear trajectory.
        self.records = [
            {
                "jd_tdb": 2460000.0,
                "position_m": (1000.0, 2000.0, 3000.0),
                "velocity_m_s": (1.0, 2.0, 3.0),
            },
            {
                "jd_tdb": 2460001.0,
                "position_m": (87400.0, 174800.0, 262200.0),
                "velocity_m_s": (1.0, 2.0, 3.0),
            },
        ]

    def test_midpoint_interpolation(self):
        result = interpolate_state(
            self.records,
            2460000.5
        )

        expected_position = (44200.0, 88400.0, 132600.0)
        expected_velocity = (1.0, 2.0, 3.0)

        for actual, expected in zip(
            result["position_m"], expected_position
        ):
            self.assertAlmostEqual(actual, expected, places=6)

        for actual, expected in zip(
            result["velocity_m_s"], expected_velocity
        ):
            self.assertAlmostEqual(actual, expected, places=6)

    def test_start_endpoint(self):
        result = interpolate_state(self.records, 2460000.0)

        self.assertEqual(
            result["position_m"],
            self.records[0]["position_m"]
        )

    def test_end_endpoint(self):
        result = interpolate_state(self.records, 2460001.0)

        self.assertEqual(
            result["position_m"],
            self.records[1]["position_m"]
        )

    def test_reject_out_of_range_time(self):
        with self.assertRaises(ValueError):
            interpolate_state(self.records, 2459999.0)

        with self.assertRaises(ValueError):
            interpolate_state(self.records, 2460002.0)

    def test_reject_single_record(self):
        with self.assertRaises(ValueError):
            interpolate_state(self.records[:1], 2460000.0)

    def test_reject_duplicate_dates(self):
        invalid_records = [
            self.records[0],
            self.records[0],
        ]

        with self.assertRaises(ValueError):
            interpolate_state(invalid_records, 2460000.0)

    def test_reject_invalid_position_vector(self):
        invalid_records = [
            self.records[0],
            {
                **self.records[1],
                "position_m": (1.0, 2.0),
            },
        ]

        with self.assertRaises(ValueError):
            interpolate_state(invalid_records, 2460000.5)

    def test_reject_non_finite_position(self):
        invalid_records = [
            self.records[0],
            {
                **self.records[1],
                "position_m": (float("nan"), 2.0, 3.0),
            },
        ]

        with self.assertRaises(ValueError):
            interpolate_state(invalid_records, 2460000.5)


if __name__ == "__main__":
    unittest.main()
