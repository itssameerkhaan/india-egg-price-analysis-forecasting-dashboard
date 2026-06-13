# Quick Start

This project now collects two related datasets:

- Egg prices from the E2NECC website using `egg_scraper.py`
- Weather data from the Open-Meteo archive API using `weather_scraper.py`
- Festival/holiday dates using `festival_generator.py`

All data scripts read dates and output settings from `config.ini`.

## 1. Check Configuration

Open `config.ini` and set the date range:

```ini
[Scraping]
start_date = 2015-01-01
end_date = 2025-01-01
years_back = 5
```

Rules:

- If `start_date` is set, the scrapers use `start_date` and `end_date`.
- If `start_date` is blank, they use `years_back`.
- If both are blank, they fall back to `days_back`.

Set the output folder and formats:

```ini
[Output]
output_dir = D:\egg_price_procject\output
save_formats = csv
```

Use `csv`, `excel`, or `pivot`. You can combine them:

```ini
save_formats = csv, excel, pivot
```

## 2. Run Egg Price Scraper

From the `data_scrap` folder:

```bash
python egg_scraper.py
```

Output files:

- `output/egg_price_data.csv`
- `output/egg_price_data.xlsx`
- `output/egg_price_pivot.xlsx`

The egg scraper uses Microsoft Edge WebDriver. If the site changes or Selenium cannot find a button, run:

```bash
python inspect_website.py
```

For a small test first:

```bash
python test_scraper.py
```

## 3. Run Weather Scraper

From the `data_scrap` folder:

```bash
python weather_scraper.py
```

Output files:

- `output/india_weather_data.csv`
- `output/india_weather_data.xlsx`
- `output/india_weather_pivot.xlsx`

Weather columns:

```text
state,date,tavg,tmin,tmax,prcp,latitude,longitude
```

The weather scraper gets state coordinates from `[WeatherCities]` in `config.ini`.

## 4. Generate Festival Dates

From the `data_scrap` folder:

```bash
python festival_generator.py
```

Output files:

- `output/india_festival_dates.csv`
- `output/india_festival_dates.xlsx`

Festival columns:

```text
Date,festival_name,Year,Month,Day
```

The festival generator uses the same `[Scraping]` date range as egg and weather.

## Common Changes

Run browser hidden for egg scraping:

```ini
[Scraping]
headless = True
```

Change weather API timing:

```ini
[Weather]
request_delay = 2.0
retry_wait = 65
timeout = 30
max_retries = 3
```

Add or edit a weather location:

```ini
[WeatherCities]
delhi = 28.6139, 77.2090
```

Change festival settings:

```ini
[Festival]
country = IN
subdiv =
language =
```

## Recommended Workflow

1. Edit `config.ini`.
2. Run `python test_scraper.py` to check egg scraping.
3. Run `python egg_scraper.py` for egg prices.
4. Run `python weather_scraper.py` for weather.
5. Run `python festival_generator.py` for festival dates.
6. Check `D:\egg_price_procject\output`.

For the full reference, read `README.md`.
