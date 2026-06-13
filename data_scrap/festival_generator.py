import os
import sys
import configparser
from datetime import datetime, timedelta

import pandas as pd


sys.stdout.reconfigure(line_buffering=True)

try:
    import holidays
except ImportError as exc:
    raise ImportError(
        "Missing dependency: holidays. Install it with "
        "`pip install holidays` or `pip install -r requirements.txt`."
    ) from exc


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.ini")


def load_config(config_file=CONFIG_FILE):
    """Load generator settings from config.ini."""
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
    default_formats = {"csv", "excel"}
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


def get_festival_settings(config):
    festival = config["Festival"] if config.has_section("Festival") else {}
    return {
        "country": (festival.get("country", "") or "IN").strip(),
        "subdiv": (festival.get("subdiv", "") or "").strip() or None,
        "language": (festival.get("language", "") or "").strip() or None,
    }


def generate_festival_dataframe(start_date, end_date, country="IN", subdiv=None, language=None):
    """Generate holiday/festival dates within the configured date range."""
    years = range(start_date.year, end_date.year + 1)
    holiday_calendar = holidays.country_holidays(
        country,
        subdiv=subdiv,
        years=years,
        language=language,
    )

    rows = []
    for date, name in sorted(holiday_calendar.items()):
        date_text = date.strftime("%Y-%m-%d")
        if start_date.date() <= date <= end_date.date():
            rows.append(
                {
                    "Date": date_text,
                    "festival_name": name,
                    "Year": date.year,
                    "Month": date.month,
                    "Day": date.day,
                }
            )

    return pd.DataFrame(rows, columns=["Date", "festival_name", "Year", "Month", "Day"])


def save_data(df, output_dir="output", save_formats=None):
    """Save festival dates using configured output formats."""
    if save_formats is None:
        save_formats = {"csv", "excel"}

    os.makedirs(output_dir, exist_ok=True)

    csv_file = os.path.join(output_dir, "india_festival_dates.csv")
    excel_file = os.path.join(output_dir, "india_festival_dates.xlsx")

    if "csv" in save_formats:
        df.to_csv(csv_file, index=False)
        print(f"\nCSV saved: {csv_file}")

    if "excel" in save_formats or "xlsx" in save_formats:
        df.to_excel(excel_file, index=False, engine="openpyxl")
        print(f"Excel saved: {excel_file}")


def main():
    """Generate Indian festival/holiday dates using config.ini settings."""
    config = load_config()
    output = config["Output"] if config.has_section("Output") else {}

    start, end = get_scrape_range(config)
    output_dir = output.get("output_dir", "output")
    save_formats = get_save_formats(config)
    settings = get_festival_settings(config)

    print(f"\nGenerating festival dates from {start.date()} to {end.date()}")
    print(f"Country: {settings['country']}")
    if settings["subdiv"]:
        print(f"Subdivision: {settings['subdiv']}")

    df = generate_festival_dataframe(
        start_date=start,
        end_date=end,
        country=settings["country"],
        subdiv=settings["subdiv"],
        language=settings["language"],
    )

    print(f"Festival rows: {len(df)}")
    if len(df) > 0:
        print("\nSample festival data:")
        print(df.head(10))
        save_data(df, output_dir=output_dir, save_formats=save_formats)
    else:
        print("No festival dates found for the configured range.")


if __name__ == "__main__":
    main()
