import unittest

from ephemeris import interpolate_state


class TestEphemeris(unittest.TestCase):

    def setUp(self):
        self.records = [
            {
                "jd_tdb": 2460000.0,
                "position_m": (1000.0, 2000.0, 3000.0),
                "velocity_m_s": (10.0, 20.0, 30.0),
            },
            {
                "jd_tdb": 2460001.0,
                "position_m": (2000.0, 3000.0, 4000.0),
                "velocity_m_s": (20.0, 30.0, 40.0),
            },
        ]

    def test_midpoint_interpolation(self):
        result = interpolate_state(
            self.records, 2460000.5
        )

        self.assertEqual(
            result["position_m"],
            (1500.0, 2500.0, 3500.0)
        )

        self.assertEqual(
            result["velocity_m_s"],
            (15.0, 25.0, 35.0)
        )

    def test_reject_out_of_range_time(self):
        with self.assertRaises(ValueError):
            interpolate_state(self.records, 2459999.0)

    def test_reject_single_record(self):
        with self.assertRaises(ValueError):
            interpolate_state(self.records[:1], 2460000.0)


if __name__ == "__main__":
    unittest.main()
