"""
Helper script to inspect the website structure and identify the correct selectors.
Run this to understand the layout of the page before running the main scraper.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.edge.service import Service
import os

EDGE_DRIVER_PATH = r"C:\edgedriver\msedgedriver.exe"

def inspect_website():
    """Inspect the website structure"""
    if not os.path.exists(EDGE_DRIVER_PATH):
        raise FileNotFoundError(
            f"Microsoft Edge WebDriver not found at: {EDGE_DRIVER_PATH}"
        )

    options = webdriver.EdgeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(executable_path=EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=options)
    
    url = "https://www.e2necc.com/home/eggprice"
    
    print(f"Opening {url}...")
    driver.get(url)
    time.sleep(3)
    
    print("\n" + "="*60)
    print("WEBPAGE STRUCTURE INSPECTION")
    print("="*60)
    
    # Get page source
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Look for input elements (year, month, day)
    print("\n1. LOOKING FOR DATE INPUT FIELDS:")
    print("-" * 40)
    
    inputs = soup.find_all('input', type='text')
    for i, inp in enumerate(inputs[:10]):  # Show first 10
        print(f"  Input {i}: {inp.get('id', 'N/A')} | Name: {inp.get('name', 'N/A')} | Placeholder: {inp.get('placeholder', 'N/A')}")
    
    # Look for buttons
    print("\n2. LOOKING FOR BUTTONS:")
    print("-" * 40)
    
    buttons = soup.find_all('button')
    for i, btn in enumerate(buttons):
        text = btn.get_text(strip=True)
        if text:  # Only show buttons with text
            print(f"  Button {i}: Text='{text}' | ID={btn.get('id', 'N/A')} | Class={btn.get('class', 'N/A')}")
    
    # Look for input buttons
    print("\n3. LOOKING FOR INPUT BUTTONS:")
    print("-" * 40)
    
    input_buttons = soup.find_all('input', type='button')
    for i, inp in enumerate(input_buttons):
        print(f"  Input Button {i}: Value='{inp.get('value', 'N/A')}' | ID={inp.get('id', 'N/A')}")
    
    # Look for tables
    print("\n4. LOOKING FOR TABLES:")
    print("-" * 40)
    
    tables = soup.find_all('table')
    print(f"  Total tables found: {len(tables)}")
    
    for i, table in enumerate(tables):
        rows = table.find_all('tr')
        print(f"  Table {i}: {len(rows)} rows")
        # Show first 2 rows
        for j, row in enumerate(rows[:2]):
            cols = row.find_all(['td', 'th'])
            col_texts = [col.get_text(strip=True)[:20] for col in cols]
            print(f"    Row {j}: {col_texts}")
    
    # Look for divs with IDs
    print("\n5. LOOKING FOR IMPORTANT DIVS:")
    print("-" * 40)
    
    divs = soup.find_all('div', id=True)
    important_ids = ['panel', 'pan', 'container', 'form', 'data', 'table', 'sheet']
    
    for div in divs:
        div_id = div.get('id', '')
        if any(important in div_id.lower() for important in important_ids):
            print(f"  Div ID: {div_id}")
    
    # Save a copy of the HTML for manual inspection
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("\n Full page HTML saved to: page_source.html")
    
    # Get page title
    print("\n6. PAGE INFORMATION:")
    print("-" * 40)
    print(f"  Page Title: {driver.title}")
    
    driver.quit()
    print("\n" + "="*60)
    print("Inspection complete!")
    print("="*60)


if __name__ == "__main__":
    inspect_website()
