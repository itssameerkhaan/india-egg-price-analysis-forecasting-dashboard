"""
Advanced usage examples for egg price, weather, and festival data.

These functions are examples. Import this file in Python and call the function
you want to run, or uncomment a call at the bottom.
"""

import os
from datetime import datetime, timedelta

import pandas as pd

from egg_scraper import EggPriceScraper, get_save_formats, get_scrape_range, load_config
from festival_generator import generate_festival_dataframe, get_festival_settings, save_data
from weather_scraper import WeatherScraper, get_weather_settings, parse_locations


OUTPUT_DIR = r"D:\egg_price_procject\output"


def example_1_egg_custom_date_range():
    """Scrape egg prices for a specific date range."""
    scraper = EggPriceScraper(headless=True)

    try:
        start = datetime(2023, 1, 1)
        end = datetime(2023, 12, 31)
        df = scraper.scrape_data_by_date_range(start, end)
        scraper.save_data(df, output_dir=os.path.join(OUTPUT_DIR, "egg_2023"))
    finally:
        scraper.close()


def example_2_egg_from_config():
    """Run egg scraping with the current config.ini settings."""
    config = load_config()
    start, end = get_scrape_range(config)
    save_formats = get_save_formats(config)
    output_dir = config["Output"].get("output_dir", OUTPUT_DIR)
    headless = config["Scraping"].get("headless", "False").lower() == "true"

    scraper = EggPriceScraper(headless=headless)

    try:
        df = scraper.scrape_data_by_date_range(start, end)
        scraper.save_data(df, output_dir=output_dir, save_formats=save_formats)
    finally:
        scraper.close()


def example_3_weather_from_config():
    """Run weather scraping with the current config.ini settings."""
    config = load_config()
    start, end = get_scrape_range(config)
    save_formats = get_save_formats(config)
    output_dir = config["Output"].get("output_dir", OUTPUT_DIR)
    locations = parse_locations(config)

    scraper = WeatherScraper(**get_weather_settings(config))
    df = scraper.scrape_data_by_date_range(locations, start, end)

    if not df.empty:
        scraper.save_data(df, output_dir=output_dir, save_formats=save_formats)


def example_4_weather_small_location_set():
    """Fetch weather for only a few locations while testing."""
    start = datetime(2024, 1, 1)
    end = datetime(2024, 1, 31)
    locations = {
        "Delhi": (28.6139, 77.2090),
        "Maharashtra": (19.0760, 72.8777),
        "Tamil Nadu": (13.0827, 80.2707),
    }

    scraper = WeatherScraper(request_delay=1, retry_wait=10, max_retries=2)
    df = scraper.scrape_data_by_date_range(locations, start, end)

    if not df.empty:
        scraper.save_data(df, output_dir=os.path.join(OUTPUT_DIR, "weather_test"))


def example_5_analyze_egg_prices():
    """Load and analyze saved egg price data."""
    df = pd.read_csv(os.path.join(OUTPUT_DIR, "egg_price_data.csv"))

    print("Egg price statistics")
    print("=" * 50)
    print(df["Price"].describe())

    print("\nAverage price by city:")
    print(df.groupby("City")["Price"].mean().sort_values(ascending=False))

    print("\nHighest prices:")
    print(df.nlargest(10, "Price")[["Category", "City", "Price", "Date"]])


def example_6_festivals_from_config():
    """Generate festival dates with the current config.ini settings."""
    config = load_config()
    start, end = get_scrape_range(config)
    output_dir = config["Output"].get("output_dir", OUTPUT_DIR)
    save_formats = get_save_formats(config)
    settings = get_festival_settings(config)

    df = generate_festival_dataframe(
        start_date=start,
        end_date=end,
        country=settings["country"],
        subdiv=settings["subdiv"],
        language=settings["language"],
    )
    save_data(df, output_dir=output_dir, save_formats=save_formats)


def example_7_analyze_weather():
    """Load and analyze saved weather data."""
    df = pd.read_csv(os.path.join(OUTPUT_DIR, "india_weather_data.csv"))

    print("Weather statistics")
    print("=" * 50)
    print(df[["tavg", "tmin", "tmax", "prcp"]].describe())

    print("\nAverage temperature by state:")
    print(df.groupby("state")["tavg"].mean().sort_values(ascending=False))

    print("\nRainiest states by total precipitation:")
    print(df.groupby("state")["prcp"].sum().sort_values(ascending=False).head(10))


def example_8_join_egg_weather_and_festivals_by_date():
    """Join egg, weather, and festival data by date for exploratory analysis."""
    egg = pd.read_csv(os.path.join(OUTPUT_DIR, "egg_price_data.csv"))
    weather = pd.read_csv(os.path.join(OUTPUT_DIR, "india_weather_data.csv"))
    festivals = pd.read_csv(os.path.join(OUTPUT_DIR, "india_festival_dates.csv"))

    egg["Date"] = pd.to_datetime(egg["Date"])
    weather["date"] = pd.to_datetime(weather["date"])
    festivals["Date"] = pd.to_datetime(festivals["Date"])

    merged = egg.merge(
        weather,
        left_on="Date",
        right_on="date",
        how="left",
    )
    merged = merged.merge(
        festivals[["Date", "festival_name"]],
        on="Date",
        how="left",
    )

    merged.to_csv(
        os.path.join(OUTPUT_DIR, "egg_weather_festival_joined_by_date.csv"),
        index=False,
    )
    print(f"Joined rows: {len(merged)}")


def example_9_export_to_extra_formats():
    """Export saved data to JSON and HTML for sharing."""
    os.makedirs(os.path.join(OUTPUT_DIR, "exports"), exist_ok=True)

    egg = pd.read_csv(os.path.join(OUTPUT_DIR, "egg_price_data.csv"))
    weather = pd.read_csv(os.path.join(OUTPUT_DIR, "india_weather_data.csv"))
    festivals = pd.read_csv(os.path.join(OUTPUT_DIR, "india_festival_dates.csv"))

    egg.to_json(
        os.path.join(OUTPUT_DIR, "exports", "egg_price_data.json"),
        orient="records",
        indent=2,
    )
    weather.to_json(
        os.path.join(OUTPUT_DIR, "exports", "india_weather_data.json"),
        orient="records",
        indent=2,
    )
    festivals.to_json(
        os.path.join(OUTPUT_DIR, "exports", "india_festival_dates.json"),
        orient="records",
        indent=2,
    )
    egg.head(500).to_html(
        os.path.join(OUTPUT_DIR, "exports", "egg_price_sample.html"),
        index=False,
    )
    weather.head(500).to_html(
        os.path.join(OUTPUT_DIR, "exports", "weather_sample.html"),
        index=False,
    )
    festivals.head(500).to_html(
        os.path.join(OUTPUT_DIR, "exports", "festival_sample.html"),
        index=False,
    )

    print("Exports written to output/exports")


def example_10_incremental_egg_scraping():
    """Append new egg price rows after the latest saved date."""
    path = os.path.join(OUTPUT_DIR, "egg_price_data.csv")
    if not os.path.exists(path):
        print("No existing egg data. Run egg_scraper.py first.")
        return

    existing_df = pd.read_csv(path)
    last_date = pd.to_datetime(existing_df["Date"]).max()
    start_date = last_date + timedelta(days=1)
    end_date = datetime.now()

    if start_date > end_date:
        print("Egg data is already up to date.")
        return

    scraper = EggPriceScraper(headless=True)

    try:
        new_df = scraper.scrape_data_by_date_range(start_date, end_date)
        combined = pd.concat([existing_df, new_df], ignore_index=True)
        combined = combined.drop_duplicates(
            subset=["Category", "City", "Date"],
            keep="last",
        )
        combined.to_csv(path, index=False)
        print(f"Added {len(new_df)} new rows.")
    finally:
        scraper.close()


if __name__ == "__main__":
    print("Advanced Examples")
    print("=" * 50)
    print("1. example_1_egg_custom_date_range()")
    print("2. example_2_egg_from_config()")
    print("3. example_3_weather_from_config()")
    print("4. example_4_weather_small_location_set()")
    print("5. example_5_analyze_egg_prices()")
    print("6. example_6_festivals_from_config()")
    print("7. example_7_analyze_weather()")
    print("8. example_8_join_egg_weather_and_festivals_by_date()")
    print("9. example_9_export_to_extra_formats()")
    print("10. example_10_incremental_egg_scraping()")
    print("\nImport this file and call the example you want to run.")
