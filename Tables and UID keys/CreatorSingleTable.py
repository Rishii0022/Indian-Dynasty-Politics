import os
import re
import pandas as pd

#Change path in 4 places.

csv_path = r"C:\Users\Rishi\Desktop\final dashboard\Scrapped data\PC split recent\Andaman & Nicobar Islands.csv"
ac_no_column = "ac no"

state_map = {
    "Andhra":"AP",
    "Kerala":"KL",
    "Tripura" :"TR",
    "Arunachal":"AR",
    "Madhya Pradesh":"MP",
    "Uttarakhand":"UK",
    "Assam":"AS",
    "Maharashtra":"MH",
    "Uttar Pradesh":"UP",
    "Bihar":"BR",
    "Manipur":"MN",
    "West Bengal":"WB",
    "Chhattisgarh":"CG",
    "Meghalaya":"ML",
    "Goa":"GA",
    "Mizoram":"MZ",
    "Andaman and Nicobar Islands":"AN",
    "Gujarat":"GJ",
    "Nagaland":"NL",
    "Chandigarh":"CH",
    "Haryana":"HR",
    "Orissa":"OR",
    "Dadra and Nagar Haveli":"DH",
    "HimachalPradesh":"HP",
    "Punjab":"PB",
    "Daman and Diu":"DD",
    "JammuKashmir":"JK",
    "Rajasthan":"RJ",
    "Delhi":"DL",
    "Jharkhand":"JH",
    "Sikkim":"SK",
    "Lakshadweep":"LD",
    "Karnataka":"KA",
    "TamilNadu":"TN",
    "Pondicherry": "PY",
    "Telangana":"TG",

}

state_map = {k.lower(): v for k, v in state_map.items()}

df = pd.read_csv(r"C:\Users\Rishi\Desktop\final dashboard\Scrapped data\PC split recent\Andaman & Nicobar Islands.csv")

# ---- PARSE FILE NAME ----
filename = os.path.basename(r"C:\Users\Rishi\Desktop\final dashboard\Scrapped data\PC split recent\Andaman & Nicobar Islands.csv").lower()

# state code
state_key = filename.split("_")[0]
state_code = state_map[state_key]

# year
year = re.search(r"\d{4}", filename).group()

# election type
election_type = "AC" if "_ac" in filename else "PC"

# ---- CREATE UID COLUMN ----
df["UID"] = (
    state_code
    + year
    + election_type
    + df[ac_no_column].astype(int).astype(str).str.zfill(2)
)

# ---- SAVE BACK TO SAME FILE ----
df.to_csv(r"C:\Users\Rishi\Desktop\final dashboard\Scrapped data\PC split recent\Andaman & Nicobar Islands.csv", index=False)
