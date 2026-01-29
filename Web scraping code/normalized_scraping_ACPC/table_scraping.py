import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

# Nested dictionary to hold tables by state and year
state_year_dfs = {}


def parse_table(page_source, state_name, year_value):


    soup = BeautifulSoup(page_source, "lxml")
    tables = soup.find_all("table")

    if not tables:
        print(f"No tables found for {state_name} {year_value}.")
        return None

    chosen_index = 1

    # Check table at index 2
    if len(tables) > 2:
        df_test = pd.read_html(StringIO(str(tables[2])))[0]
        if df_test.shape[0] >= 25:
            chosen_index = 2


    df = pd.read_html(StringIO(str(tables[chosen_index])))[0]

    # Save CSV first
    filename = f"{state_name.replace(' ', '')}_{year_value}_ac.csv"
    df.to_csv(filename, index=False)
    print(f"Saved table to {filename}")

    # --- Delete first row from CSV ---
    df = pd.read_csv(filename, header=None)  # Load without header
    df = df.iloc[1:]  # Drop first row
    df.to_csv(filename, index=False, header=False)  # Save back
    print(f"First row deleted from {filename}")

    df = pd.read_csv(filename)
    df = df.drop(df.columns[0], axis=1)
    df.to_csv(filename, index=False)
    print(f"First column deleted from {filename}")

    df = pd.read_csv(filename)
    if df['AC Name'].duplicated().any():  # Check if duplicates exist in 'AC Name'
        df = df.drop_duplicates(subset=['AC Name'])  # Remove duplicates based on column
        df.to_csv(filename, index=False)  # Save back
        print(f"Duplicates removed based on 'AC Name' in {filename}")
    else:
        print("No duplicates found in 'AC Name'; skipping duplicate removal.")








