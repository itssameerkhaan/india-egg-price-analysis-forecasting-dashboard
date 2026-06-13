# Final Instructions

The project is configured to scrape egg prices, weather data, and festival dates into the same output folder.

## Project Layout

```text
data_scrap/
  egg_scraper.py          E2NECC egg price scraper
  weather_scraper.py      Open-Meteo weather scraper
  festival_generator.py   Festival/holiday date generator
  test_scraper.py         Short egg scraper test
  inspect_website.py      E2NECC page inspector
  advanced_examples.py    Analysis/export examples
  project_guide.py        Console project overview
  config.ini              Shared configuration
  requirements.txt        Dependencies
  README.md               Full documentation
  QUICKSTART.md           Short guide
```

## Configure Once

Edit `config.ini`:

```ini
[Scraping]
start_date = 2015-01-01
end_date = 2025-01-01
years_back = 5

[Output]
output_dir = D:\egg_price_procject\output
save_formats = csv
```

The egg scraper, weather scraper, and festival generator all use `[Scraping]` and `[Output]`.

## Run Egg Price Data

```bash
python test_scraper.py
python egg_scraper.py
```

Expected output:

- `egg_price_data.csv`
- `egg_price_data.xlsx`
- `egg_price_pivot.xlsx`

Egg data columns include:

```text
Category,City,Price,Day,Month,Year,Date
```

## Run Weather Data

```bash
python weather_scraper.py
```

Expected output:

- `india_weather_data.csv`
- `india_weather_data.xlsx`
- `india_weather_pivot.xlsx`

Weather data columns:

```text
state,date,tavg,tmin,tmax,prcp,latitude,longitude
```

## Run Festival Dates

```bash
python festival_generator.py
```

Expected output:

- `india_festival_dates.csv`
- `india_festival_dates.xlsx`

Festival data columns:

```text
Date,festival_name,Year,Month,Day
```

## Weather Locations

Weather locations are configured here:

```ini
[WeatherCities]
andhra_pradesh = 16.5062, 80.6480
delhi = 28.6139, 77.2090
```

Add a new location with:

```ini
location_name = latitude, longitude
```

## Common Issues

Egg website changed:

```bash
python inspect_website.py
```

Edge WebDriver missing:

- Confirm `C:\edgedriver\msedgedriver.exe` exists.
- Confirm Microsoft Edge is installed.

Weather API rate limit:

- Increase `[Weather] request_delay`.
- Increase `[Weather] retry_wait`.

Festival dependency missing:

```bash
pip install -r requirements.txt
```

No Excel output:

- Set `save_formats = csv, excel`.
- Confirm `openpyxl` is installed.

## Recommended Run Order

1. Edit `config.ini`.
2. Run `python project_guide.py` if you want a console overview.
3. Run `python test_scraper.py`.
4. Run `python egg_scraper.py`.
5. Run `python weather_scraper.py`.
6. Run `python festival_generator.py`.
7. Analyze files in `D:\egg_price_procject\output`.
