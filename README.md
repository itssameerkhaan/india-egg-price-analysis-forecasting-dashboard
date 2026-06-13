# Egg Price Forecasting Project

An end-to-end Python project for collecting Indian egg price data, enriching it with weather and festival features, training forecasting models, and viewing model results in a local web dashboard.

## Project Objective

The objective of this project is to build a practical egg price forecasting system that can help analyze historical market behavior and estimate future egg prices for selected Indian cities. Egg prices can change because of seasonality, demand patterns, festivals, weather, and recent market movement, so this project combines price history with external factors to create better forecasting features.

The project covers the full workflow: collecting raw data, preparing clean city-wise datasets, engineering time-series features, training machine learning models, validating forecast quality, and presenting the results through charts and a local web dashboard. The main goal is to make egg price trends easier to understand and support short-term forecasting decisions using data-driven methods.

## Overview

This project contains:

- Data scraping scripts for NECC egg prices, Indian festivals, and weather data
- Feature engineering for city-level egg price forecasting
- XGBoost and baseline model training/validation workflows
- Recursive forecast outputs and comparison charts
- A lightweight local web app for running the pipeline and viewing results


## Dashboard Preview

## Dashboard Preview

![Dashboard Preview](https://github.com/user-attachments/assets/8db7c731-a256-42fd-aa2e-1081678d22c9)

## Forecast Chart Example

![Forecast Chart](https://github.com/user-attachments/assets/3b4fe5f6-ef54-4c2a-8297-3a13819cf2ec)

![Forecast Chart 2](https://github.com/user-attachments/assets/50486e3e-9561-4d0d-a5a7-11d0b8843f4a)


## Project Structure

```text
egg_price_procject/
|-- analysis/
|   |-- feature_extraction.py
|   |-- model_training_comparison.py
|   |-- recursive_forecast.py
|   |-- rough_model_training/
|   `-- analysis_chart/
|-- application/
|   |-- backend/
|   |   |-- server.py
|   |   `-- start_server.ps1
|   `-- web/
|       |-- index.html
|       |-- app.js
|       `-- styles.css
|-- data_scrap/
|   |-- egg_scraper.py
|   |-- festival_generator.py
|   |-- weather_scraper.py
|   `-- requirements.txt
|-- documents/
|-- output/
|-- run_pipeline.ps1
|-- run.bat
`-- requirements.txt
```

## Features

- Scrapes historical egg price data
- Generates Indian festival/holiday calendar data
- Collects weather features such as temperature and rainfall
- Creates lag, rolling average, calendar, festival, and market trend features
- Trains forecasting models with time-series validation
- Produces daily, weekly, and monthly comparison files
- Generates interactive Plotly HTML charts
- Provides a local dashboard for running scraping/modeling jobs

## Tech Stack

- Python 3.11+
- pandas, NumPy
- scikit-learn
- XGBoost
- Plotly
- Selenium
- BeautifulSoup
- PowerShell scripts for Windows automation

## Setup

Clone the repository:

```powershell
git clone https://github.com/<your-username>/<your-repository-name>.git
cd <your-repository-name>
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the Data Pipeline

The data pipeline runs these scripts in order:

1. `data_scrap/egg_scraper.py`
2. `data_scrap/festival_generator.py`
3. `data_scrap/weather_scraper.py`
4. `analysis/feature_extraction.py`

Run it with:

```powershell
.\run_pipeline.ps1
```

Or on Windows Command Prompt:

```bat
run.bat
```

## Train and Validate the Model

Run the main recursive validation workflow:

```powershell
python analysis\model_training_comparison.py --city Barwala
```

Run the improved multi-horizon experiment:

```powershell
python analysis\rough_model_training\improved_egg_price_forecast.py --city Barwala --horizons all --save-html
```

Useful options:

```powershell
python analysis\rough_model_training\improved_egg_price_forecast.py --city Delhi --horizons 1,2,3,4 --split-date 2025-01-01 --save-html
```

## Run the Web Dashboard

Start the local backend:

```powershell
python application\backend\server.py
```

Then open:

```text
http://127.0.0.1:8080
```

The dashboard can show available cities, model metrics, generated charts, dataset previews, and pipeline job logs.

## Outputs

Generated files are written mainly to:

- `output/main_data/` for city-level feature datasets
- `output/forecast/` for forecast results
- `output/forecast/compare/` for validation metrics and comparisons
- `analysis/analysis_chart/` for interactive model comparison charts
- `analysis/rough_model_training/` for experiment charts

These generated artifacts are ignored by Git by default. Regenerate them locally by running the pipeline and model scripts.

## Notes

- The scripts are currently optimized for a Windows/PowerShell workflow.
- Some existing scripts use local paths from the original project directory. If you clone the project into a different folder, update paths in `run_pipeline.ps1`, `run.bat`, or run the Python files directly from the project root.
- Selenium scraping may require a compatible browser and driver setup.





