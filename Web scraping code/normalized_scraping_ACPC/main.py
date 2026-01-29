#test1.py
from scraping1 import get_vidhan_sabha_page
from webscraping import parse_table
import pandas as pd
import time

states = ["State Name"]  # add all states
years = ["add election years"] # add years
years = sorted(years, key=int)  # sort numerically, ascending

print("Years list:", years)
for state in states:
    for year in years:
        print(f"Scraping {state} - {year} ...")

        try:
            # Step 1: get page source
            page_source = get_vidhan_sabha_page(state, year)

            # If page_source is empty or None, skip this year
            if not page_source or page_source.strip() == "":
                print(f"No page found for {state} {year}, skipping.")
                continue

            # Step 2: parse the second table
            df = parse_table(page_source, state, year)

        except Exception as e:
            print(f" Error scraping {state} - {year}: {e}")
            continue  # move to next year/state

        time.sleep(1)  # prevent server overload
