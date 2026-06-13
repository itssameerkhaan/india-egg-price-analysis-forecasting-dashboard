import os
import sys
import time
import configparser
from datetime import datetime, timedelta

import pandas as pd
import requests


sys.stdout.reconfigure(line_buffering=True)

OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.ini")


DEFAULT_LOCATIONS = {
    "Andhra Pradesh": (16.5062, 80.6480),
    "Arunachal Pradesh": (27.0844, 93.6053),
    "Assam": (26.1445, 91.7362),
    "Bihar": (25.5941, 85.1376),
    "Chhattisgarh": (21.2514, 81.6296),
    "Goa": (15.4909, 73.8278),
    "Gujarat": (23.0225, 72.5714),
    "Haryana": (30.7333, 76.7794),
    "Himachal Pradesh": (31.1048, 77.1734),
    "Jharkhand": (23.3441, 85.3096),
    "Karnataka": (12.9716, 77.5946),
    "Kerala": (8.5241, 76.9366),
    "Madhya Pradesh": (23.2599, 77.4126),
    "Maharashtra": (19.0760, 72.8777),
    "Manipur": (24.8170, 93.9368),
    "Meghalaya": (25.5788, 91.8933),
    "Mizoram": (23.7271, 92.7176),
    "Nagaland": (25.6751, 94.1086),
    "Odisha": (20.2961, 85.8245),
    "Punjab": (30.7333, 76.7794),
    "Rajasthan": (26.9124, 75.7873),
    "Sikkim": (27.3314, 88.6138),
    "Tamil Nadu": (13.0827, 80.2707),
    "Telangana": (17.3850, 78.4867),
    "Tripura": (23.8315, 91.2868),
    "Uttar Pradesh": (26.8467, 80.9462),
    "Uttarakhand": (30.3165, 78.0322),
    "West Bengal": (22.5726, 88.3639),
    "Andaman and Nicobar Islands": (11.6234, 92.7265),
    "Chandigarh": (30.7333, 76.7794),
    "Dadra and Nagar Haveli and Daman and Diu": (20.3974, 72.8328),
    "Delhi": (28.6139, 77.2090),
    "Jammu and Kashmir": (34.0837, 74.7973),
    "Ladakh": (34.1526, 77.5770),
    "Lakshadweep": (10.5667, 72.6417),
    "Puducherry": (11.9416, 79.8083),
}


def load_config(config_file=CONFIG_FILE):
    """Load scraper settings from config.ini."""
    config = configparser.ConfigParser()
    loaded_files = config.read(config_file)
    if not loaded_files:
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    return config


def parse_config_date(value):
    """Parse YYYY-MM-DD config dates. Empty values return None."""
    value = (value or "").strip()
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d")


def subtract_years(date, years):
    """Return the same date N years earlier, handling leap years."""
    try:
        return date.replace(year=date.year - years)
    except ValueError:
        return date.replace(year=date.year - years, day=28)


def get_scrape_range(config):
    """Get start/end dates from config, using years_back when start_date is empty."""
    scraping = config["Scraping"] if config.has_section("Scraping") else {}

    end_date = parse_config_date(scraping.get("end_date", "")) or datetime.now()
    start_date = parse_config_date(scraping.get("start_date", ""))
    if start_date:
        return start_date, end_date

    years_back = (scraping.get("years_back", "") or "").strip()
    if years_back:
        return subtract_years(end_date, int(years_back)), end_date

    days_back = int((scraping.get("days_back", "") or "365").strip())
    return end_date - timedelta(days=days_back), end_date


def get_save_formats(config):
    """Get output formats from config. Empty or missing values use defaults."""
    default_formats = {"csv", "excel", "pivot"}
    if not config.has_section("Output"):
        return default_formats

    raw_formats = (config["Output"].get("save_formats", "") or "").strip()
    if not raw_formats:
        return default_formats

    formats = {
        item.strip().lower()
        for item in raw_formats.split(",")
        if item.strip()
    }
    valid_formats = {"csv", "excel", "xlsx", "pivot"}
    unknown_formats = formats - valid_formats
    if unknown_formats:
        print(
            "Warning: Ignoring unknown save format(s): "
            f"{', '.join(sorted(unknown_formats))}"
        )

    selected_formats = formats & valid_formats
    return selected_formats or default_formats


class WeatherScraper:
    def __init__(self, request_delay=2.0, retry_wait=65, timeout=30, max_retries=3):
        self.request_delay = float(request_delay)
        self.retry_wait = int(retry_wait)
        self.timeout = int(timeout)
        self.max_retries = int(max_retries)
        self.failed_locations = []

    def scrape_data_by_date_range(self, locations, start_date, end_date):
        """Fetch daily Open-Meteo archive data for all configured locations."""
        all_data = []
        total_locations = len(locations)

        print(f"\n{'=' * 60}")
        print(
            "Fetching weather data from "
            f"{start_date.date()} to {end_date.date()}"
        )
        print(f"Total locations to process: {total_locations}")
        print(f"{'=' * 60}\n")

        for index, (location, coords) in enumerate(locations.items(), start=1):
            lat, lon = coords
            print(f"[{index}/{total_locations}] Fetching {location}...")

            df = self.fetch_location(location, lat, lon, start_date, end_date)
            if df is not None and not df.empty:
                all_data.append(df)
                print(f"Done {location}: {len(df)} rows\n")
            else:
                self.failed_locations.append(location)
                print(f"No data saved for {location}\n")

            time.sleep(self.request_delay)

        if not all_data:
            print("No weather data fetched.")
            return pd.DataFrame()

        final_df = pd.concat(all_data, ignore_index=True)
        final_df = final_df.sort_values(["state", "date"]).reset_index(drop=True)

        print("\nDataFrame Summary:")
        print(f"  - Total rows: {len(final_df)}")
        print(f"  - Date range: {final_df['date'].min()} to {final_df['date'].max()}")
        print(f"  - Locations: {final_df['state'].nunique()}")
        print(f"  - Columns: {list(final_df.columns)}")

        return final_df

    def fetch_location(self, location, lat, lon, start_date, end_date):
        """Fetch one location, waiting and retrying when the API rate-limits."""
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "daily": ",".join(
                [
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "temperature_2m_mean",
                    "precipitation_sum",
                ]
            ),
            "timezone": "auto",
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.get(
                    OPEN_METEO_ARCHIVE_URL,
                    params=params,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                data = response.json()

                if "daily" not in data:
                    reason = data.get("reason", "daily data missing from response")
                    print(
                        f"API response did not include daily data for {location}: "
                        f"{reason}"
                    )
                    if attempt < self.max_retries:
                        print(f"Waiting {self.retry_wait} seconds before retry...")
                        time.sleep(self.retry_wait)
                        continue
                    return None

                return self.create_location_dataframe(location, lat, lon, data["daily"])

            except requests.RequestException as exc:
                print(f"Request error for {location}: {exc}")
                if attempt < self.max_retries:
                    print(f"Waiting {self.retry_wait} seconds before retry...")
                    time.sleep(self.retry_wait)
                    continue
                return None

            except ValueError as exc:
                print(f"JSON parse error for {location}: {exc}")
                return None

        return None

    @staticmethod
    def create_location_dataframe(location, lat, lon, daily):
        """Convert Open-Meteo daily JSON into the project weather DataFrame."""
        df = pd.DataFrame(
            {
                "date": daily.get("time", []),
                "tavg": daily.get("temperature_2m_mean", []),
                "tmin": daily.get("temperature_2m_min", []),
                "tmax": daily.get("temperature_2m_max", []),
                "prcp": daily.get("precipitation_sum", []),
            }
        )
        df["state"] = location
        df["latitude"] = lat
        df["longitude"] = lon
        return df[
            [
                "state",
                "date",
                "tavg",
                "tmin",
                "tmax",
                "prcp",
                "latitude",
                "longitude",
            ]
        ]

    def save_data(self, df, output_dir="output", save_formats=None):
        """Save weather DataFrame using the same output formats as egg data."""
        if save_formats is None:
            save_formats = {"csv", "excel"}

        os.makedirs(output_dir, exist_ok=True)

        csv_file = os.path.join(output_dir, "india_weather_data.csv")
        excel_file = os.path.join(output_dir, "india_weather_data.xlsx")

        if "csv" in save_formats:
            df.to_csv(csv_file, index=False)
            print(f"\nCSV saved: {csv_file}")

        if "excel" in save_formats or "xlsx" in save_formats:
            df.to_excel(excel_file, index=False, engine="openpyxl")
            print(f"Excel saved: {excel_file}")

        if "pivot" in save_formats:
            pivot_file = os.path.join(output_dir, "india_weather_pivot.xlsx")
            pivot_df = df.pivot_table(
                index="date",
                columns="state",
                values="tavg",
                aggfunc="first",
            )
            pivot_df.to_excel(pivot_file, engine="openpyxl")
            print(f"Average temperature pivot saved: {pivot_file}")


def parse_locations(config):
    """Load locations from [WeatherCities], falling back to default India list."""
    if not config.has_section("WeatherCities"):
        return DEFAULT_LOCATIONS

    locations = {}
    for location, value in config.items("WeatherCities"):
        try:
            lat_text, lon_text = value.split(",", 1)
            title = location.replace("_", " ").title()
            locations[title] = (float(lat_text.strip()), float(lon_text.strip()))
        except ValueError:
            print(f"Warning: ignoring invalid WeatherCities entry: {location}={value}")

    return locations or DEFAULT_LOCATIONS


def get_weather_settings(config):
    weather = config["Weather"] if config.has_section("Weather") else {}
    return {
        "request_delay": float((weather.get("request_delay", "") or "2").strip()),
        "retry_wait": int((weather.get("retry_wait", "") or "65").strip()),
        "timeout": int((weather.get("timeout", "") or "30").strip()),
        "max_retries": int((weather.get("max_retries", "") or "3").strip()),
    }


def main():
    """Run the weather scraper using config.ini settings."""
    config = load_config()
    output = config["Output"] if config.has_section("Output") else {}

    start, end = get_scrape_range(config)
    output_dir = output.get("output_dir", "output")
    save_formats = get_save_formats(config)
    locations = parse_locations(config)

    scraper = WeatherScraper(**get_weather_settings(config))
    df = scraper.scrape_data_by_date_range(
        locations=locations,
        start_date=start,
        end_date=end,
    )

    if len(df) > 0:
        print("\nSample of weather data:")
        print(df.head(10))
        print("\n...")
        print(df.tail(10))
        scraper.save_data(
            df,
            output_dir=output_dir,
            save_formats=save_formats,
        )

    print("\nFailed Locations:")
    print(scraper.failed_locations)


if __name__ == "__main__":
    main()
