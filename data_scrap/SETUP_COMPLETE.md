# Setup Complete

The data scraping project is ready for egg price, weather, and festival date collection.

## Installed Dependencies

```text
selenium==4.15.2
pandas==2.1.4
beautifulsoup4==4.12.2
requests==2.31.0
lxml==4.9.3
openpyxl==3.1.2
holidays==0.82
```

Microsoft Edge WebDriver is expected at:

```text
C:\edgedriver\msedgedriver.exe
```

## Scripts

| Script | Description |
|--------|-------------|
| `egg_scraper.py` | Scrapes egg prices from E2NECC |
| `weather_scraper.py` | Fetches daily weather from Open-Meteo |
| `festival_generator.py` | Generates festival/holiday dates |
| `test_scraper.py` | Runs a small egg price test |
| `inspect_website.py` | Helps debug E2NECC page structure |
| `advanced_examples.py` | Shows analysis and export examples |
| `project_guide.py` | Prints a project overview |

## Shared Configuration

Both production scrapers use:

```ini
[Scraping]
start_date =
end_date =
years_back = 5
days_back =

[Output]
output_dir = D:\egg_price_procject\output
save_formats = csv
```

The egg scraper uses Selenium settings from `[Scraping]` and `[Website]`.

The weather scraper uses API settings from `[Weather]` and coordinates from `[WeatherCities]`.
The festival generator uses settings from `[Festival]`.

## Run Commands

From `data_scrap`:

```bash
python test_scraper.py
python egg_scraper.py
python weather_scraper.py
python festival_generator.py
```

## Output Files

Egg prices:

- `egg_price_data.csv`
- `egg_price_data.xlsx`
- `egg_price_pivot.xlsx`

Weather:

- `india_weather_data.csv`
- `india_weather_data.xlsx`
- `india_weather_pivot.xlsx`

Festivals:

- `india_festival_dates.csv`
- `india_festival_dates.xlsx`

Only the formats listed in `save_formats` are written.

## Data Shapes

Egg price rows:

```text
Category,City,Price,Day,Month,Year,Date
```

Weather rows:

```text
state,date,tavg,tmin,tmax,prcp,latitude,longitude
```

Festival rows:

```text
Date,festival_name,Year,Month,Day
```

## Next Steps

1. Edit `config.ini`.
2. Run `python test_scraper.py` to verify Selenium and the egg website.
3. Run `python egg_scraper.py`.
4. Run `python weather_scraper.py`.
5. Run `python festival_generator.py`.
6. Open the files in the configured output folder.
