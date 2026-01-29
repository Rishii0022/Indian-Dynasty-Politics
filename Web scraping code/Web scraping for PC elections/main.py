#main.py
from scraping_code import parse_table
from webdriver_code import get_lok_sabha_page
import time

states = ["State Name"]  # add all state names
years = ["add election years"] # add all election years
years = sorted(years, key=int)

print("Years list:", years)
for state in states:
    for year in years:
        print(f"Scraping {state} - {year} ...")

        try:
            # get page source
            page_source = get_lok_sabha_page(state, year)

            # If page_source is empty or None, skip this year
            if not page_source or page_source.strip() == "":
                print(f"No page found for {state} {year}, skipping.")
                continue

            # parse the second table
            df = parse_table(page_source, state, year)

        except Exception as e:
            print(f" Error scraping {state} - {year}: {e}")
            continue

        time.sleep(1)