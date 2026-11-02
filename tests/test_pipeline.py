import unittest

from src.main import DATA, build_features


class EnergyPipelineTests(unittest.TestCase):
    def test_weather_join_and_prior_window_anomaly(self):
        rows = build_features(DATA / "meter_readings.csv", DATA / "weather.csv")
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[-1]["temperature_c"], "3.2")
        self.assertEqual(rows[-1]["is_anomaly"], "1")


if __name__ == "__main__":
    unittest.main()
