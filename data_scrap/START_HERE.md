# Start Here

This folder contains the data collection tools for the egg price project.

You can collect:

- Historical egg prices by city/category
- Historical daily weather by Indian state/UT
- Indian festival/holiday dates

All data scripts use the same `config.ini` date range and output folder.

## Main Commands

Run these from `data_scrap`:

```bash
python test_scraper.py
python egg_scraper.py
python weather_scraper.py
python festival_generator.py
python project_guide.py
```

Use `test_scraper.py` before a long egg-price scrape. Use `weather_scraper.py` directly for Open-Meteo data.

## Files

| File | Purpose |
|------|---------|
| `egg_scraper.py` | Main E2NECC egg price scraper |
| `weather_scraper.py` | Open-Meteo weather archive scraper |
| `festival_generator.py` | Festival/holiday date generator |
| `test_scraper.py` | Small egg scraper test run |
| `inspect_website.py` | Website structure/debug helper for E2NECC |
| `advanced_examples.py` | Example analysis and export workflows |
| `project_guide.py` | Console overview of this project |
| `config.ini` | Shared scraper settings |
| `requirements.txt` | Python dependencies |
| `README.md` | Complete reference |
| `QUICKSTART.md` | Fast setup and run guide |

## Configuration

Edit `config.ini` first:

```ini
[Scraping]
start_date = 2015-01-01
end_date = 2025-01-01
years_back = 5

[Output]
output_dir = D:\egg_price_procject\output
save_formats = csv
```

The egg scraper also uses:

```ini
headless = False
max_wait_time = 15
```

The weather scraper also uses:

```ini
[Weather]
request_delay = 2.0
retry_wait = 65
timeout = 30
max_retries = 3
```

Weather locations are in `[WeatherCities]`.

The festival generator also uses:

```ini
[Festival]
country = IN
subdiv =
language =
```

## Output

Egg price output:

- `egg_price_data.csv`
- `egg_price_data.xlsx`
- `egg_price_pivot.xlsx`

Weather output:

- `india_weather_data.csv`
- `india_weather_data.xlsx`
- `india_weather_pivot.xlsx`

Festival output:

- `india_festival_dates.csv`
- `india_festival_dates.xlsx`

The actual formats depend on `save_formats`.

## What To Run First

For egg prices:

```bash
python test_scraper.py
python egg_scraper.py
```

For weather:

```bash
python weather_scraper.py
```

For festival dates:

```bash
python festival_generator.py
```

For help:

```bash
python project_guide.py
```

## Troubleshooting

If egg scraping cannot find page elements:

```bash
python inspect_website.py
```

If weather scraping pauses, the Open-Meteo API may be rate limiting. The scraper waits and retries using `[Weather] retry_wait` and `max_retries`.
