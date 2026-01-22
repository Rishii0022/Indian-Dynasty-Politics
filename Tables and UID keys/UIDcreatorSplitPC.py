import pandas as pd
import os
import re

# ---- CONFIG ----
folder_path = r"C:\Users\Rishi\Desktop\final dashboard\Scrapped data\PC split recent"
pc_no_column = "No"
YEAR = "2024"
ELECTION_TYPE = "PC"

state_map = {
    "Andhra Pradesh":"AP",
    "Kerala":"KL",
    "Tripura":"TR",
    "Arunachal Pradesh":"AR",
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
    "Andaman & Nicobar Islands":"AN",
    "Gujarat":"GJ",
    "Nagaland":"NL",
    "Chandigarh":"CH",
    "Haryana":"HR",
    "Orissa":"OR",
    "Dadra & Nagar Haveli":"DH",
    "Himachal Pradesh":"HP",
    "Punjab":"PB",
    "Daman & Diu":"DD",
    "Jammu & Kashmir":"JK",
    "Rajasthan":"RJ",
    "Delhi":"DL",
    "Jharkhand":"JH",
    "Sikkim":"SK",
    "Lakshadweep":"LD",
    "Karnataka":"KA",
    "Tamil Nadu":"TN",
    "Pondicherry":"PY",
    "Telangana":"TG",
    "Ladakh":"LA"
}

# normalize state map
state_map = {
    k.lower().replace(" ", "").replace("&", ""): v
    for k, v in state_map.items()
}

# ---- PROCESS FILES ----
for file in os.listdir(folder_path):
    if not file.lower().endswith(".csv"):
        continue

    csv_path = os.path.join(folder_path, file)

    # ---- STATE FROM FILENAME ----
    state_name = os.path.splitext(file)[0]
    state_key = state_name.lower().replace(" ", "").replace("&", "")

    if state_key not in state_map:
        raise KeyError(f"State not found in map: {file}")

    state_code = state_map[state_key]

    # ---- LOAD CSV ----
    df = pd.read_csv(csv_path)

    # normalize columns
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(".", "", regex=False)
    )

    # ---- FIND PC NUMBER COLUMN ----
    pc_variants = {"No", "no"}
    pc_no_column = next(
        (c for c in df.columns if c.replace(" ", "") in pc_variants),
        None
    )

    if pc_no_column is None:
        raise KeyError(f"PC No column not found in {file}")

    # ---- REMOVE OLD UID COLUMNS ----
    uid_cols = [c for c in df.columns if c.lower().startswith("uid")]
    df.drop(columns=uid_cols, inplace=True)

    # ---- CREATE UID ----
    mask = df[pc_no_column].notna()

    df.loc[mask, "UID"] = (
        state_code
        + YEAR
        + ELECTION_TYPE
        + df.loc[mask, pc_no_column]
            .astype(int)
            .astype(str)
            .str.zfill(2)
    )

    # ---- SAVE ----
    df.to_csv(csv_path, index=False)
