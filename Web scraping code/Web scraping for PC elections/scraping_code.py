#scraping_code.py
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

# Nested dictionary to hold tables by state and year
state_year_dfs = {}


def parse_table(page_source, state_name, year_value):

# Scrape table at index 2 if it exists AND has >= 30 rows, otherwise use table at index 1


    # Parse HTML
    soup = BeautifulSoup(page_source, "lxml")
    tables = soup.find_all("table")

    if not tables:
        print(f"No tables found for {state_name} {year_value}.")
        return None

    # Default table index
    chosen_index = 1

    # Check table at index 2
    if len(tables) > 2:
        df_test = pd.read_html(StringIO(str(tables[2])))[0]
        if df_test.shape[0] >= 100:
            chosen_index = 2

    # Read the chosen table
    df = pd.read_html(StringIO(str(tables[chosen_index])))[0]

    # Save CSV without modifying table
    filename = f"{state_name.replace(' ', '')}_{year_value}_pc.csv"
    df.to_csv(filename, index=False)
    print(f"Saved table to {filename}")