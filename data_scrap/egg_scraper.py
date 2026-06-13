import os
import sys
import time
import configparser
from datetime import datetime, timedelta

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

import logging
logging.getLogger('selenium').setLevel(logging.CRITICAL)


sys.stdout.reconfigure(line_buffering=True)

EDGE_DRIVER_PATH = r"C:\edgedriver\msedgedriver.exe"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.ini")


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


class EggPriceScraper:
    def __init__(self, headless=False, driver_path=EDGE_DRIVER_PATH):
        """Initialize the Selenium WebDriver."""
        if not os.path.exists(driver_path):
            raise FileNotFoundError(
                f"Microsoft Edge WebDriver not found at: {driver_path}"
            )

        options = webdriver.EdgeOptions()

        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Disable Edge/Selenium logging
        options.add_experimental_option(
            'excludeSwitches',
            ['enable-logging']
        )

        service = Service(executable_path=driver_path)
        self.driver = webdriver.Edge(service=service, options=options)
        self.url = "https://www.e2necc.com/home/eggprice"
        self.wait = WebDriverWait(self.driver, 15)

    def scrape_data_by_date_range(self, start_date=None, end_date=None, step_days=1, progress_interval=1):
        """
        Scrape NECC egg price data for a date range.

        The website returns a full month of daily prices in one table, so this
        submits one request per month and extracts only the requested dates.
        The step_days argument is kept for compatibility with old examples.
        """
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=365)

        self.driver.get(self.url)
        time.sleep(3)

        all_data = []
        current_month = datetime(end_date.year, end_date.month, 1)
        last_month = datetime(start_date.year, start_date.month, 1)
        total_months = self.month_count(last_month, current_month)
        total_processed = 0
        started_at = time.perf_counter()

        print(f"\n{'=' * 60}")
        print(f"Scraping egg price data from {start_date.date()} to {end_date.date()}")
        print(f"Total months to process: {total_months}")
        print(f"{'=' * 60}\n")

        while current_month >= last_month:
            try:
                self.set_date(current_month)
                self.click_get_sheet()
                time.sleep(0.8)

                data = self.extract_table_data(current_month, start_date, end_date)
                all_data.extend(data)

                total_processed += 1
                if (
                    total_processed == 1
                    or total_processed % progress_interval == 0
                    or total_processed == total_months
                ):
                    elapsed = time.perf_counter() - started_at
                    seconds_per_month = elapsed / total_processed
                    remaining_months = max(total_months - total_processed, 0)
                    eta_minutes = (remaining_months * seconds_per_month) / 60
                    sys.stdout.write(
                        f"\rProgress: {total_processed}/{total_months} months "
                        f"({total_processed / total_months:.1%}), "
                        f"last month: {current_month.strftime('%Y-%m')}, "
                        f"records: {len(all_data)}, "
                        f"ETA: {eta_minutes:.1f} min"
                    )

                    sys.stdout.flush()

                current_month = self.previous_month(current_month)

            except Exception as e:
                print(
                    f"Warning: Error processing month "
                    f"{current_month.strftime('%Y-%m')}: {str(e)}"
                )
                current_month = self.previous_month(current_month)
                continue

        print(f"\nTotal months processed: {total_processed}")
        print(f"Total records extracted: {len(all_data)}")

        return self.create_dataframe(all_data)

    @staticmethod
    def month_count(start_month, end_month):
        """Return inclusive month count between two month-start datetimes."""
        return ((end_month.year - start_month.year) * 12) + end_month.month - start_month.month + 1

    @staticmethod
    def next_month(date):
        """Return the first day of the next month."""
        if date.month == 12:
            return datetime(date.year + 1, 1, 1)
        return datetime(date.year, date.month + 1, 1)

    @staticmethod
    def previous_month(date):
        """Return the first day of the previous month."""
        if date.month == 1:
            return datetime(date.year - 1, 12, 1)
        return datetime(date.year, date.month - 1, 1)

    def set_date(self, date):
        """Set the website month/year controls."""
        try:
            def find_first(selectors):
                for selector in selectors:
                    elements = self.driver.find_elements(*selector)
                    if elements:
                        return elements[0]
                return None

            def set_control_value(element, value):
                if element.tag_name.lower() == "select":
                    Select(element).select_by_value(str(value))
                else:
                    element.clear()
                    element.send_keys(str(value))

            year_input = find_first([
                (By.ID, "ddlYear"),
                (By.NAME, "ddlYear"),
                (By.ID, "year"),
                (By.NAME, "year"),
                (By.CSS_SELECTOR, "input[name='year']"),
            ])
            if year_input:
                set_control_value(year_input, date.year)
            else:
                raise Exception("Could not find year control")

            month_input = find_first([
                (By.ID, "ddlMonth"),
                (By.NAME, "ddlMonth"),
                (By.ID, "month"),
                (By.NAME, "month"),
                (By.CSS_SELECTOR, "input[name='month']"),
            ])
            if month_input:
                set_control_value(month_input, f"{date.month:02d}")
            else:
                raise Exception("Could not find month control")

            daily_radio = find_first([
                (By.CSS_SELECTOR, "input[name='rblReportType'][value='DailyReport']"),
                (By.XPATH, "//input[@type='radio' and @value='DailyReport']"),
            ])
            if daily_radio and not daily_radio.is_selected():
                daily_radio.click()

            time.sleep(0.2)

        except Exception as e:
            print(f"Error setting date: {str(e)}")
            raise

    def click_get_sheet(self):
        """Click the Get Sheet button."""
        button_selectors = [
            (By.ID, "btnReport"),
            (By.NAME, "btnReport"),
            (By.XPATH, "/html/body/div[1]/div/div[1]/table/tbody/tr[2]/td[3]/input"),
            (By.CSS_SELECTOR, "input[type='submit'][value='Get Sheet']"),
            (By.XPATH, "//input[@type='submit' and @value='Get Sheet']"),
        ]

        for selector in button_selectors:
            try:
                button = self.wait.until(EC.element_to_be_clickable(selector))
                button.click()
                return
            except Exception:
                continue

        raise Exception("Could not find Get Sheet button")

    def extract_table_data(self, month_date, start_date=None, end_date=None):
        """Extract daily city prices from the monthly table."""
        data = []
        try:
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            pan2 = soup.find(id="pan2")
            table = pan2.find("table") if pan2 else None
            if not table:
                for candidate in soup.find_all("table"):
                    if "Name Of Zone / Day" in candidate.get_text(" ", strip=True):
                        table = candidate
                        break

            if not table:
                return data

            rows = table.find_all("tr")
            if not rows:
                return data

            header_cells = rows[0].find_all(["th", "td"])
            day_columns = []
            for column_index, cell in enumerate(header_cells):
                text = cell.get_text(strip=True)
                if text.isdigit():
                    day = int(text)
                    if 1 <= day <= 31:
                        day_columns.append((column_index, day))

            category = None
            for row in rows[1:]:
                cols = row.find_all("td")
                if not cols:
                    continue

                if len(cols) == 1 or cols[0].has_attr("colspan"):
                    category_text = cols[0].get_text(" ", strip=True)
                    if category_text:
                        category = category_text
                    continue

                city_name = cols[0].get_text(" ", strip=True)
                if not city_name:
                    continue

                for column_index, day in day_columns:
                    if column_index >= len(cols):
                        continue

                    try:
                        actual_date = datetime(month_date.year, month_date.month, day)
                    except ValueError:
                        continue

                    if start_date and actual_date.date() < start_date.date():
                        continue
                    if end_date and actual_date.date() > end_date.date():
                        continue

                    price_text = cols[column_index].get_text(strip=True).replace(",", "")
                    if not price_text or price_text == "-":
                        continue

                    try:
                        price = float(price_text)
                    except ValueError:
                        continue

                    data.append({
                        "Category": category,
                        "City": city_name,
                        "Price": price,
                        "Day": actual_date.day,
                        "Month": actual_date.month,
                        "Year": actual_date.year,
                        "Date": actual_date.strftime("%Y-%m-%d"),
                    })

        except Exception as e:
            print(f"Error extracting table data: {str(e)}")

        return data

    def create_dataframe(self, data):
        """Create a pandas DataFrame from scraped data."""
        if len(data) == 0:
            print("No data scraped!")
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
        df = df.sort_values(
            ["Year", "Month", "Day", "Category", "City"],
            ascending=[False, False, False, True, True],
        ).reset_index(drop=True)
        df = df.drop_duplicates(subset=["Category", "City", "Date"], keep="first")

        print("\nDataFrame Summary:")
        print(f"  - Total rows: {len(df)}")
        print(f"  - Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"  - Cities: {df['City'].nunique()}")
        print(f"  - Columns: {list(df.columns)}")

        return df

    def save_data(self, df, output_dir="output", save_formats=None):
        """Save DataFrame using selected formats."""
        if save_formats is None:
            save_formats = {"csv", "excel", "pivot"}

        os.makedirs(output_dir, exist_ok=True)

        csv_file = os.path.join(output_dir, "egg_price_data.csv")
        excel_file = os.path.join(output_dir, "egg_price_data.xlsx")

        if "csv" in save_formats:
            df.to_csv(csv_file, index=False)
            print(f"\nCSV saved: {csv_file}")

        if "excel" in save_formats or "xlsx" in save_formats:
            df.to_excel(excel_file, index=False, engine="openpyxl")
            print(f"Excel saved: {excel_file}")

        if "pivot" in save_formats:
            pivot_file = os.path.join(output_dir, "egg_price_pivot.xlsx")
            pivot_index = ["Year", "Month", "Day", "Date"]
            if "Category" in df.columns:
                pivot_index.insert(0, "Category")
            pivot_df = df.pivot_table(
                index=pivot_index,
                columns="City",
                values="Price",
                aggfunc="first",
            )
            pivot_df.to_excel(pivot_file, engine="openpyxl")
            print(f"Pivot table saved: {pivot_file}")

    def close(self):
        """Close the WebDriver."""
        self.driver.quit()
        print("\nBrowser closed.")


def main():
    """Run the scraper using config.ini settings."""
    config = load_config()
    scraping = config["Scraping"] if config.has_section("Scraping") else {}
    output = config["Output"] if config.has_section("Output") else {}
    logging = config["Logging"] if config.has_section("Logging") else {}

    start, end = get_scrape_range(config)
    headless = str(scraping.get("headless", "False")).strip().lower() == "true"
    progress_interval = int((logging.get("progress_interval", "") or "1").strip())
    output_dir = output.get("output_dir", "output")
    save_formats = get_save_formats(config)

    scraper = EggPriceScraper(headless=headless)

    try:
        df = scraper.scrape_data_by_date_range(
            start_date=start,
            end_date=end,
            progress_interval=progress_interval,
        )

        if len(df) > 0:
            print("\nSample of scraped data:")
            print(df.head(10))
            print("\n...")
            print(df.tail(10))
            scraper.save_data(
                df,
                output_dir=output_dir,
                save_formats=save_formats,
            )

    except Exception as e:
        print(f"\nError during scraping: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        scraper.close()


if __name__ == "__main__":
    main()
