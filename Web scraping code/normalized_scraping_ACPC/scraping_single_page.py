from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import time

# INPUT
state_name = "State Name"
year_value = "Election year"
url = "url"

# Selenium setup
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get(url)
time.sleep(3)  # wait for JS to load

soup = BeautifulSoup(driver.page_source, "lxml")
driver.quit()

# Find tables
tables = soup.find_all("table")
print(f"Found {len(tables)} tables")

if len(tables) < 0:
    print("Less than 2 tables found even after JS load.")
    exit()

# Extract 2nd table
df = pd.read_html(StringIO(str(tables[1])))[0]

# Save file
filename = f"{state_name.replace(' ', '')}_{year_value}_ac.csv"
df.to_csv(filename, index=False)

print(f"Saved → {filename}")






