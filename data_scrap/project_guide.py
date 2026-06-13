#!/usr/bin/env python3
"""
Console overview for the egg price, weather, and festival data project.
"""


def print_header(text):
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print(f"{'=' * 70}\n")


def print_section(title):
    print(f"\n{'-' * 70}")
    print(f"  {title}")
    print(f"{'-' * 70}\n")


def get_file_description(filename):
    descriptions = {
        "egg_scraper.py": "Main E2NECC egg price scraper",
        "weather_scraper.py": "Open-Meteo weather scraper for Indian states/UTs",
        "festival_generator.py": "Festival/holiday date generator",
        "test_scraper.py": "Small egg scraper verification run",
        "inspect_website.py": "Website structure analyzer for E2NECC",
        "advanced_examples.py": "Analysis, export, and custom workflow examples",
        "config.ini": "Shared configuration for dates, output, and locations",
        "requirements.txt": "Python package dependencies",
        "README.md": "Complete project reference",
        "QUICKSTART.md": "Short setup and run guide",
        "START_HERE.md": "First-read overview",
        "SETUP_COMPLETE.md": "Setup summary",
        "FINAL_INSTRUCTIONS.md": "Run checklist and common issues",
        ".gitignore": "Ignored generated files and caches",
    }
    return descriptions.get(filename, "Project file")


def main():
    print_header("DATA SCRAPING PROJECT OVERVIEW")

    print("This project collects egg price, weather, and festival date data.")
    print("Both production scrapers read shared settings from config.ini.")

    print_section("PROJECT FILES")

    files = [
        ("egg_scraper.py", "EGG DATA"),
        ("weather_scraper.py", "WEATHER DATA"),
        ("festival_generator.py", "FESTIVALS"),
        ("test_scraper.py", "TESTING"),
        ("inspect_website.py", "DEBUGGING"),
        ("advanced_examples.py", "EXAMPLES"),
        ("config.ini", "CONFIGURATION"),
        ("requirements.txt", "DEPENDENCIES"),
        ("README.md", "DOCUMENTATION"),
        ("QUICKSTART.md", "GETTING STARTED"),
        ("START_HERE.md", "OVERVIEW"),
        ("SETUP_COMPLETE.md", "SETUP"),
        ("FINAL_INSTRUCTIONS.md", "CHECKLIST"),
        (".gitignore", "GIT"),
    ]

    for filename, category in files:
        print(f"  {filename:<24} [{category:<15}] {get_file_description(filename)}")

    print_section("COMMON COMMANDS")

    commands = [
        ("python project_guide.py", "Show this overview"),
        ("python test_scraper.py", "Test egg scraping with a small date range"),
        ("python egg_scraper.py", "Scrape egg prices using config.ini"),
        ("python weather_scraper.py", "Fetch weather data using config.ini"),
        ("python festival_generator.py", "Generate festival dates using config.ini"),
        ("python inspect_website.py", "Inspect E2NECC when egg scraping breaks"),
    ]

    for command, purpose in commands:
        print(f"  {command:<28} {purpose}")

    print_section("CONFIGURATION")

    print("Edit config.ini before long runs.")
    print("Shared settings:")
    print("  [Scraping] start_date, end_date, years_back, days_back")
    print("  [Output] output_dir, save_formats")
    print("\nEgg-specific settings:")
    print("  [Scraping] headless, max_wait_time")
    print("  [Website] url, request_delay")
    print("\nWeather-specific settings:")
    print("  [Weather] request_delay, retry_wait, timeout, max_retries")
    print("  [WeatherCities] location_name = latitude, longitude")
    print("\nFestival-specific settings:")
    print("  [Festival] country, subdiv, language")

    print_section("OUTPUT FILES")

    print("Egg price outputs:")
    print("  output/egg_price_data.csv")
    print("  output/egg_price_data.xlsx")
    print("  output/egg_price_pivot.xlsx")
    print("\nWeather outputs:")
    print("  output/india_weather_data.csv")
    print("  output/india_weather_data.xlsx")
    print("  output/india_weather_pivot.xlsx")
    print("\nFestival outputs:")
    print("  output/india_festival_dates.csv")
    print("  output/india_festival_dates.xlsx")

    print_section("DATA COLUMNS")

    print("Egg price:")
    print("  Category, City, Price, Day, Month, Year, Date")
    print("\nWeather:")
    print("  state, date, tavg, tmin, tmax, prcp, latitude, longitude")
    print("\nFestivals:")
    print("  Date, festival_name, Year, Month, Day")

    print_section("RECOMMENDED START")

    print("1. Edit config.ini")
    print("2. Run python test_scraper.py")
    print("3. Run python egg_scraper.py")
    print("4. Run python weather_scraper.py")
    print("5. Run python festival_generator.py")
    print("6. Read README.md for details")


if __name__ == "__main__":
    main()
