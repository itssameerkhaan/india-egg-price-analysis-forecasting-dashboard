# Read Me First

Start here if you are opening the project for the first time.

## What This Project Does

It collects three datasets:

- Egg price history from E2NECC
- Daily weather history from Open-Meteo
- Festival/holiday dates from the `holidays` package

The datasets are saved into the same output folder so they can be joined later by date and location/state.

## First File To Edit

Edit:

```text
config.ini
```

Important settings:

```ini
[Scraping]
start_date = 2015-01-01
end_date = 2025-01-01
years_back = 5

[Output]
output_dir = D:\egg_price_procject\output
save_formats = csv
```

## First Commands To Run

```bash
python project_guide.py
python test_scraper.py
python egg_scraper.py
python weather_scraper.py
python festival_generator.py
```

Use `test_scraper.py` before a long egg price scrape.

## Output

Egg prices:

```text
egg_price_data.csv
egg_price_data.xlsx
egg_price_pivot.xlsx
```

Weather:

```text
india_weather_data.csv
india_weather_data.xlsx
india_weather_pivot.xlsx
```

Festivals:

```text
india_festival_dates.csv
india_festival_dates.xlsx
```

The active output formats are controlled by `save_formats`.

## When Something Breaks

Egg scraper page issue:

```bash
python inspect_website.py
```

Weather API issue:

- Check your internet connection.
- Increase `[Weather] request_delay`.
- Check the `Failed Locations` printed at the end.

Festival dependency issue:

```bash
pip install -r requirements.txt
```

## Documentation Map

| File | Use |
|------|-----|
| `QUICKSTART.md` | Fast run instructions |
| `README.md` | Full reference |
| `SETUP_COMPLETE.md` | Setup summary |
| `FINAL_INSTRUCTIONS.md` | Run order and common issues |
| `advanced_examples.py` | Code examples |
| `project_guide.py` | Console overview |

## Short Version

Set dates in `config.ini`, then run:

```bash
python egg_scraper.py
python weather_scraper.py
python festival_generator.py
```
