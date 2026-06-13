"""
Quick test script to verify the egg scraper before running a longer scrape.
Run this first to make sure everything is configured correctly.
"""

from datetime import datetime, timedelta
from egg_scraper import EggPriceScraper

def test_scraper():
    """Test the scraper with a small date range"""
    
    print("\n" + "="*60)
    print("EGG PRICE SCRAPER - TEST RUN")
    print("="*60)
    print("\nTesting with the last 7 days of data...\n")
    
    scraper = EggPriceScraper(headless=False)
    
    try:
        # Test with last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        print(f"Test Date Range: {start_date.date()} to {end_date.date()}\n")
        
        # Run scraper
        df = scraper.scrape_data_by_date_range(start_date, end_date)
        
        if len(df) > 0:
            print("\n" + "="*60)
            print("TEST SUCCESSFUL!")
            print("="*60)
            print(f"\nDataFrame shape: {df.shape}")
            print(f"Columns: {list(df.columns)}\n")
            
            print("Sample data (first 5 rows):")
            print(df.head())
            
            print("\n Scraper is working correctly!")
            print("\nNext steps:")
            print("1. Review the sample data above")
            print("2. Edit config.ini if you want a different date range")
            print("3. Run: python egg_scraper.py")
            print("4. Optional weather data: python weather_scraper.py")
            print("5. Optional festival dates: python festival_generator.py")
            print("6. Results will be saved to the configured output folder\n")
            
            # Option to save test data
            save_test = input("Save this test data (y/n): ").lower()
            if save_test == 'y':
                scraper.save_data(df, output_dir='test_output')
                print(" Test data saved to test_output/\n")
        else:
            print("\n No data was scraped. Checking website structure...\n")
            print("Run 'python inspect_website.py' to diagnose the issue.")
    
    except Exception as e:
        print(f"\n Error during test: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Run 'python inspect_website.py' to check the page structure")
        print("2. Check if the website is accessible")
        print("3. Review the error message above for details\n")
        import traceback
        traceback.print_exc()
    
    finally:
        scraper.close()


if __name__ == "__main__":
    test_scraper()
