# Egg Price And Weather Data Scrapers

This project collects historical egg price, weather, and festival/holiday data for analysis.

## What It Collects

Egg prices:

- Source: `https://www.e2necc.com/home/eggprice`
- Script: `egg_scraper.py`
- Method: Selenium browser automation plus HTML table parsing
- Output: city/category/date price rows

Weather:

- Source: Open-Meteo archive API
- Script: `weather_scraper.py`
- Method: `requests` API calls
- Output: daily temperature and precipitation rows by configured state/location

Festivals/holidays:

- Source: Python `holidays` package
- Script: `festival_generator.py`
- Method: local calendar generation
- Output: Indian holiday/festival dates for the configured date range

## Files

| File | Purpose |
|------|---------|
| `egg_scraper.py` | Main egg price scraper |
| `weather_scraper.py` | Main weather scraper |
| `festival_generator.py` | Festival/holiday date generator |
| `test_scraper.py` | Small egg scraper test |
| `inspect_website.py` | E2NECC website inspector/debug tool |
| `advanced_examples.py` | Examples for scraping, exporting, and analysis |
| `project_guide.py` | Console overview of scripts and outputs |
| `config.ini` | Shared settings |
| `requirements.txt` | Python dependencies |
| `QUICKSTART.md` | Short start guide |
| `START_HERE.md` | First-read overview |
| `SETUP_COMPLETE.md` | Setup summary |
| `FINAL_INSTRUCTIONS.md` | Run checklist and common issues |

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

The egg scraper also expects Microsoft Edge WebDriver at:

```text
C:\edgedriver\msedgedriver.exe
```

The weather scraper does not need Selenium or a browser.
The festival generator does not need network access.

## Configuration

Most behavior is controlled by `config.ini`.

### Shared Date Range

```ini
[Scraping]
start_date = 2015-01-01
end_date = 2025-01-01
years_back = 5
days_back =
```

Date priority:

1. If `start_date` is set, use `start_date` and `end_date`.
2. If `start_date` is blank and `years_back` is set, count back from `end_date` or today.
3. If both are blank, use `days_back`.

### Shared Output

```ini
[Output]
output_dir = D:\egg_price_procject\output
save_formats = csv
overwrite = False
```

Valid `save_formats`:

```text
csv, excel, xlsx, pivot
```

Examples:

```ini
save_formats = csv
save_formats = csv, excel
save_formats = csv, excel, pivot
```

### Egg Scraper Settings

```ini
[Scraping]
step_days = 1
headless = False
max_wait_time = 15

[Website]
url = https://www.e2necc.com/home/eggprice
request_delay = 1.0
```

Note: the current egg scraper processes monthly tables. `step_days` is kept for compatibility with older examples.

### Weather Scraper Settings

```ini
[Weather]
request_delay = 2.0
retry_wait = 65
timeout = 30
max_retries = 3
```

Weather locations:

```ini
[WeatherCities]
delhi = 28.6139, 77.2090
maharashtra = 19.0760, 72.8777
```

Use this format:

```ini
location_name = latitude, longitude
```

If `[WeatherCities]` is removed, `weather_scraper.py` falls back to its built-in Indian states/UT list.

### Festival Generator Settings

```ini
[Festival]
country = IN
subdiv =
language =
```

`festival_generator.py` uses the same `[Scraping]` date range and `[Output]` folder as the other scripts.

## Usage

Run commands from the `data_scrap` folder.

Check the project:

```bash
python project_guide.py
```

Test egg scraping:

```bash
python test_scraper.py
```

Scrape egg prices:

```bash
python egg_scraper.py
```

Scrape weather:

```bash
python weather_scraper.py
```

Generate festival dates:

```bash
python festival_generator.py
```

Inspect the egg website if Selenium selectors break:

```bash
python inspect_website.py
```

## Output Files

Egg price files:

```text
egg_price_data.csv
egg_price_data.xlsx
egg_price_pivot.xlsx
```

Egg price columns:

```text
Category,City,Price,Day,Month,Year,Date
```

Weather files:

```text
india_weather_data.csv
india_weather_data.xlsx
india_weather_pivot.xlsx
```

Weather columns:

```text
state,date,tavg,tmin,tmax,prcp,latitude,longitude
```

Weather field meanings:

- `tavg`: daily mean temperature, degrees Celsius
- `tmin`: daily minimum temperature, degrees Celsius
- `tmax`: daily maximum temperature, degrees Celsius
- `prcp`: daily precipitation sum

Festival files:

```text
india_festival_dates.csv
india_festival_dates.xlsx
```

Festival columns:

```text
Date,festival_name,Year,Month,Day
```

## Python Examples

Load egg price data:

```python
import pandas as pd

egg = pd.read_csv(r"D:\egg_price_procject\output\egg_price_data.csv")
print(egg.groupby("City")["Price"].mean())
```

Load weather data:

```python
import pandas as pd

weather = pd.read_csv(r"D:\egg_price_procject\output\india_weather_data.csv")
print(weather.groupby("state")["tavg"].mean())
```

Load festival data:

```python
import pandas as pd

festivals = pd.read_csv(r"D:\egg_price_procject\output\india_festival_dates.csv")
print(festivals.head())
```

Join by date for analysis:

```python
egg["Date"] = pd.to_datetime(egg["Date"])
weather["date"] = pd.to_datetime(weather["date"])

merged = egg.merge(
    weather,
    left_on="Date",
    right_on="date",
    how="left",
)
```

For more examples, see `advanced_examples.py`.

## Troubleshooting

Egg scraper cannot find controls:

```bash
python inspect_website.py
```

Then check `page_source.html`.

Edge WebDriver error:

- Confirm Microsoft Edge is installed.
- Confirm `C:\edgedriver\msedgedriver.exe` exists.

No egg rows:

- Check whether the E2NECC table layout changed.
- Run a smaller date range first.

Weather API retries or missing locations:

- Check the final `Failed Locations` list.
- Increase `[Weather] request_delay`.
- Increase `[Weather] retry_wait`.
- Try fewer locations in `[WeatherCities]`.

Excel files not created:

- Set `save_formats = csv, excel`.
- Confirm `openpyxl` is installed.

Festival generator says `holidays` is missing:

```bash
pip install -r requirements.txt
```

## Recommended Workflow

1. Edit `config.ini`.
2. Run `python project_guide.py`.
3. Run `python test_scraper.py`.
4. Run `python egg_scraper.py`.
5. Run `python weather_scraper.py`.
6. Run `python festival_generator.py`.
7. Analyze the files in the configured output folder.
