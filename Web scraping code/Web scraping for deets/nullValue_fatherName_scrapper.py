from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import pandas as pd

# open the browser
chromedriver_path = r"C:\\Program Files (x86)\\chromedriver.exe"
proxy_ip = "add ip address here"

options = Options()
options.add_argument(f"--proxy-server=http://{proxy_ip}")

driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
driver.get("https://affidavit.eci.gov.in") #website url

wait = WebDriverWait(driver, 20)

form = wait.until(EC.presence_of_element_located((By.ID, "CandidateCustomFilter")))

# Add options from dropdown menus
Select(form.find_element(By.ID, "electionType")).select_by_visible_text("Election-Feb-May-2021")
time.sleep(3)

Select(form.find_element(By.ID, "election")).select_by_visible_text("AC - GENERAL")
time.sleep(3)

Select(form.find_element(By.ID, "states")).select_by_visible_text("Tamil Nadu")
time.sleep(3)

Select(wait.until(EC.presence_of_element_located((By.ID, "phase")))).select_by_index(1)
time.sleep(3)

Select(wait.until(EC.presence_of_element_located((By.ID, "constId")))).select_by_visible_text("Select Constituency")
time.sleep(2)

form.find_element(By.CSS_SELECTOR, "button.btn.search.btn-primary").click()
time.sleep(3)

# LOAD CSV
csv_path = r"C:\Users\Rishi\Desktop\final dashboard\Scrapped data\ac recent\TamilNadu_2021_ac.csv"
df = pd.read_csv(csv_path, keep_default_na=True, na_values=[""])
df.columns = df.columns.str.strip()

#use ONE consistent column name
father_col = "father/husband name"

# LOOP
for index, row in df.iterrows():

    candidate_name = str(row["winning candidate"]).strip()
    father_name_existing = row[father_col]

    # only process null rows
    if not pd.isna(father_name_existing):
        continue

    parts = candidate_name.split()

    # skip names not exactly 2 words
    if len(parts) != 2:
        print("Skipping (not 2 words):", candidate_name)
        continue

    candidate_name = f"{parts[1]} {parts[0]}"

    csv_party = row["party"].strip().lower()
    print("Processing:", candidate_name)

    search_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='search']"))
    )

    search_input.clear()
    search_input.send_keys(candidate_name)

    search_container = driver.find_element(By.CSS_SELECTOR, "div.card-header.head-affi")
    search_container.find_element(By.CSS_SELECTOR, "button[name='submitName']").click()

    time.sleep(3.5)

    try:
        details_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".details-name"))
        )
    except:
        print("Candidate not found")
        continue

    status_p = details_box.find_element(
        By.XPATH, ".//p[strong[contains(text(), 'Status')]]"
    )
    if status_p.text.replace("Status :", "").strip().lower() != "accepted":
        continue

    party_p = details_box.find_element(
        By.XPATH, ".//p[strong[contains(text(), 'Party')]]"
    )
    website_party = party_p.text.replace("Party :", "").strip().lower()

    allowed_variants_for_bjp = [
        "bharatiya janata party",
        "bharatiya janta party"
    ]

    if website_party == "bharatiya janata party":
        if csv_party not in allowed_variants_for_bjp:
            continue
    elif website_party != csv_party:
        continue

    details_box.find_element(By.LINK_TEXT, "View more").click()
    time.sleep(2)

    tabs = driver.window_handles
    driver.switch_to.window(tabs[-1])

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h3[contains(text(), 'Candidate Personal Details')]")
        )
    )

    personal_details_box = driver.find_element(By.CSS_SELECTOR, ".detail-person")

    def get_detail(label_text):
        try:
            label = personal_details_box.find_element(
                By.XPATH, f".//p[contains(text(), \"{label_text}\")]"
            )
            value = label.find_element(
                By.XPATH, "../../div[@class='col-sm-6']/p"
            )
            return value.text.strip()
        except:
            return ""

    name = get_detail("Father's / Husband's Name")
    gender = get_detail("Gender")
    age = get_detail("Age")

    # save only scraped values
    if name.strip() != "":
        df.loc[index, father_col] = name
        df.loc[index, "Gender"] = gender
        df.loc[index, "Age"] = age

    driver.close()
    driver.switch_to.window(tabs[0])

    time.sleep(0.2)

# save
df.to_csv(csv_path, index=False)

print("CSV updated for ALL candidates")
