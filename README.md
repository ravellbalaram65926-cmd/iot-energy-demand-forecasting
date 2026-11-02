# IoT / Energy Demand Forecasting with Anomaly Detection

## Problem
Forecast energy demand and flag abnormal consumption from sensor and weather data.

## Dataset and provenance

The committed meter/weather CSVs are synthetic. For a real smart-meter benchmark, see [UCI Individual Household Electric Power Consumption](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption); enrich with weather from [Open-Meteo](https://open-meteo.com/) under its applicable terms. Keep large files/API outputs under ignored `data/external/`.

## Run the ETL demo

From this directory, run `python src/main.py`. It deduplicates and sorts meter readings, validates nonnegative values, joins weather on the UTC timestamp, and computes a prior-three-reading anomaly flag without lookahead. Output is `data/gold/energy_features.csv`; paths can be overridden with `--meters`, `--weather`, and `--output`. Run checks with `python -m pytest -q tests`.

## Stack
Python, Airflow/Prefect, Parquet/Delta, Prophet or LightGBM

## Architecture
- Bronze / raw ingestion layer
- Silver / cleaned and validated data layer
- Gold / feature or serving layer
- Monitoring / validation and retraining feedback loop

## DE tasks
1. Ingest raw data with versioned file naming and timestamps.
2. Build idempotent and incremental transformations.
3. Add data quality checks and freshness alerts.
4. Create a reproducible run order using a Makefile or run script.
5. Store outputs in a warehouse, lake, or streaming sink with clear contracts.

## DS tasks
1. Run EDA and validate assumptions about seasonality, drift, and user behavior.
2. Benchmark a baseline model before trying a stronger approach.
3. Use proper time-based splits and avoid leakage.
4. Log experiments, tuning choices and key metrics.
5. Report limitations and next steps in a production-focused way.

## Deliverables
- Reproducible pipeline or app
- Tests for transformation and validation logic
- Dashboard, API, or report showing outputs
- Clear business summary with measurable impact

## Recommended repository structure
`	ext
iot-energy-demand-forecasting/
+-- README.md
+-- requirements.txt
+-- Makefile
+-- .gitignore
+-- src/
+-- tests/
+-- notebooks/
+-- docs/
`

## Resume line
Built a scheduled forecasting and anomaly-detection pipeline combining sensor and weather data.
