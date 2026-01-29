from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--start-maximized")

proxy_ip = "add ip address here"

options.add_argument(f"--proxy-server=http://{proxy_ip}")
#options.add_argument("--headless=new")
#options.add_argument("--disable-gpu")
#options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

import time
import pandas as pd

#open the browser of eci
# chromedriver_path = r"C:\\Program Files (x86)\\chromedriver.exe"

# driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
driver.get("https://affidavit.eci.gov.in")

#print(driver.page_source)


wait = WebDriverWait(driver, 20)

form = wait.until(EC.presence_of_element_located((By.ID, "CandidateCustomFilter")))

#Add options from dropdown menus
select1 = Select(form.find_element(By.ID, "electionType"))
select1.select_by_visible_text("General Election 2024")
time.sleep(3)

select2 = Select(form.find_element(By.ID, "election"))
select2.select_by_visible_text("PC - GENERAL")
time.sleep(3)

select3 = Select(form.find_element(By.ID, "states"))
select3.select_by_visible_text("West Bengal")
time.sleep(3)

phase_dropdown = wait.until(EC.presence_of_element_located((By.ID, "phase")))
Select(phase_dropdown).select_by_index(1)
time.sleep(3)

const_dropdown = wait.until(EC.presence_of_element_located((By.ID, "constId")))
Select(const_dropdown).select_by_visible_text("Select Constituency")
time.sleep(2)

filter_button = form.find_element(By.CSS_SELECTOR, "button.btn.search.btn-primary")
filter_button.click()

time.sleep(3)

# LOAD CSV (ALL CANDIDATES)
csv_path = r"C:\Users\Rishi\Desktop\lok sabha split\West Bengal.csv"
df = pd.read_csv(csv_path)


# LOOP THROUGH EVERY CANDIDATE
for index, row in df.iterrows():

# LOOP THROUGH EVERY CANDIDATE FROM A SPECIFIC INDEX
#for index, row in df.iloc[63:].iterrows():

    candidate_name = str(row["Winning Candidate"]).strip()
    csv_party = row["Party"].strip().lower()

    print("Processing:", candidate_name)

    # Search box
    search_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='search']"))
    )

    search_input.clear()
    search_input.send_keys(candidate_name)

    search_container = driver.find_element(By.CSS_SELECTOR, "div.card-header.head-affi")
    search_button = search_container.find_element(By.CSS_SELECTOR, "button[name='submitName']")
    search_button.click()

    time.sleep(3.5)

    #DETAILS BOX
    try:
        details_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".details-name"))
        )
    except:
        print("Candidate not found, skipping")
        continue

    #CHECK STATUS
    status_p = details_box.find_element(
        By.XPATH, ".//p[strong[contains(text(), 'Status')]]"
    )
    candidate_status = status_p.text.replace("Status :", "").strip().lower()

    if candidate_status != "accepted":
        print("Status not accepted, skipping")
        continue

    #CHECK PARTY
    party_p = details_box.find_element(
        By.XPATH, ".//p[strong[contains(text(), 'Party')]]"
    )

    website_party = party_p.text.replace("Party :", "").strip().lower()

    allowed_variants_for_bjp = [
        "bharatiya janata party",
        "bharatiya janta party"
    ]

    party_match = False

    #BJP CASE
    if website_party == "bharatiya janata party":
        if csv_party in allowed_variants_for_bjp:
            party_match = True

    #OTHER PARTIES MATCH EXACT
    elif website_party == csv_party:
        party_match = True

    if not party_match:
        print("Party does not match, skipping")  # changed this
        continue

    #CLICK VIEW MORE
    view_more_button = details_box.find_element(By.LINK_TEXT, "View more")
    view_more_button.click()

    time.sleep(2)


    # SWITCH TO NEW TAB
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
            label_element = personal_details_box.find_element(
                By.XPATH, f".//p[contains(text(), \"{label_text}\")]"
            )
            value_element = label_element.find_element(
                By.XPATH, "../../div[@class='col-sm-6']/p"
            )
            return value_element.text.strip()
        except:
            return ""

    name = get_detail("Father's / Husband's Name")
    gender = get_detail("Gender")
    age = get_detail("Age")

    # SAVE DETAILS TO CSV ROW   # changed this
    df.loc[index, "Father/Husband Name"] = name
    df.loc[index, "Gender"] = gender
    df.loc[index, "Age"] = age

    df.to_csv(csv_path, index=False)

    print("CSV updated")

    # CLOSE TAB AND RETURN
    driver.close()
    driver.switch_to.window(tabs[0])

    time.sleep(0.2)

print("CSV updated for ALL candidates")
