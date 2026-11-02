"""ETL demo: join hourly meter/weather data and flag prior-window outliers."""

import argparse
import csv
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
DEFAULT_OUTPUT = ROOT / "data" / "gold" / "energy_features.csv"


def build_features(meter_path: Path, weather_path: Path) -> list[dict[str, str]]:
    with meter_path.open(newline="", encoding="utf-8") as source:
        meters = list(csv.DictReader(source))
    with weather_path.open(newline="", encoding="utf-8") as source:
        weather = {row["timestamp"]: row["temperature_c"] for row in csv.DictReader(source)}
    meters.sort(key=lambda row: (row["meter_id"], row["timestamp"]))
    histories: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=3))
    seen = set()
    result = []
    for row in meters:
        key = (row["meter_id"], row["timestamp"])
        if key in seen:
            continue
        seen.add(key)
        datetime.fromisoformat(row["timestamp"])
        energy = float(row["energy_kwh"])
        if energy < 0:
            raise ValueError(f"Negative energy reading for {key}")
        if row["timestamp"] not in weather:
            raise ValueError(f"Missing weather record for {row['timestamp']}")
        history = histories[row["meter_id"]]
        baseline = sum(history) / len(history) if history else 0.0
        row.update(
            {
                "temperature_c": weather[row["timestamp"]],
                "prior_3_reading_mean": f"{baseline:.3f}",
                "is_anomaly": str(int(len(history) >= 3 and energy > 2 * baseline)),
            }
        )
        result.append(row)
        history.append(energy)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--meters", type=Path, default=DATA / "meter_readings.csv")
    parser.add_argument("--weather", type=Path, default=DATA / "weather.csv")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    rows = build_features(args.meters, args.weather)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)
    print(f"Built {len(rows)} energy feature rows at {args.output}")


if __name__ == "__main__":
    main()
