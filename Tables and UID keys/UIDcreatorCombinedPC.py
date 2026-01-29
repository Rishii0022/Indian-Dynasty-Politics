import pandas as pd
import os
import re

# Add folder path for input data
folder_path = r"folder_path"
ELECTION_TYPE = "PC"

# Goa, Daman and Diu held the same Lok Sabha elections as part of a single Union Territory from their liberation in 1961 until May 1987
# Mapped LokSabha seats containing state name Goa, Daman and Diu to DD(Daman and Diu)
# "Goa, Daman And Diu":"DD"

# Other older state names remapped to current states
#     "Uttar Pradesh [1947 - 1999]":"UP",
#     "Hyderabad":"TG",
#     "Ajmer":"RJ",
#     "Bhopal":"MP",
#     "Bihar [1947 - 1999]":"BR",
#     "Bilaspur":"CG",
#     "Bombay":"MH",
#     "Kutch":"GJ",
#     "Madhya Bharat":"MP",
#     "Madhya Pradesh [1947 - 1999]":"MP",
#     "Madras":"TN",
#     "Mysore":"KA",
#     "Patiala And East Punj":"PB",
#     "Saurashtra":"GJ",
#     "Travancore Cochin":"KL",
#     "Vindhya Pradesh":"MP",
#     "Andhra Pradesh [2014 Onwards]":"AP",
#     "Bihar [2000 Onwards]":"BR",
#     "Delhi [1977 Onwards]":"DL",
#     "Madhya Pradesh [2000 Onwards]":"MP",
#     "Uttar Pradesh [2000 Onwards]":"UP",
#     "Coorg":"KA",
#     "Laccadive, Minicoy And Amindivi Islands":"LD",
#     "Goa, Daman And Diu":"DD"



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
    "Ladakh":"LA",
    "Uttar Pradesh [1947 - 1999]":"UP",
    "Hyderabad":"TG",
    "Ajmer":"RJ",
    "Bhopal":"MP",
    "Bihar [1947 - 1999]":"BR",
    "Bilaspur":"CG",
    "Bombay":"MH",
    "Kutch":"GJ",
    "Madhya Bharat":"MP",
    "Madhya Pradesh [1947 - 1999]":"MP",
    "Madras":"TN",
    "Mysore":"KA",
    "Patiala And East Punj":"PB",
    "Saurashtra":"GJ",
    "Travancore Cochin":"KL",
    "Vindhya Pradesh":"MP",
    "Andhra Pradesh [2014 Onwards]":"AP",
    "Bihar [2000 Onwards]":"BR",
    "Delhi [1977 Onwards]":"DL",
    "Madhya Pradesh [2000 Onwards]":"MP",
    "Uttar Pradesh [2000 Onwards]":"UP",
    "Coorg":"KA",
    "Laccadive, Minicoy And Amindivi Islands":"LD",
    "Goa, Daman And Diu":"DD"

}

# normalize state keys
state_map = {
    k.lower().replace(" ", "").replace("&", ""): v
    for k, v in state_map.items()
}

# --------------------
# PROCESS FILES
# --------------------

for file in os.listdir(folder_path):

    if not file.lower().endswith(".csv"):
        continue

    csv_path = os.path.join(folder_path, file)

    # ---- YEAR FROM FILENAME ----
    match = re.search(r"\d{4}", file)
    if not match:
        raise ValueError(f"Year not found in filename: {file}")

    YEAR = match.group()

    # ---- LOAD CSV ----
    df = pd.read_csv(csv_path)

    # normalize columns
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(".", "", regex=False)
    )

    # required columns
    required = {"state", "no"}
    if not required.issubset(df.columns):
        raise KeyError(f"Missing required columns in {file}")

    # remove existing UID columns
    uid_cols = [c for c in df.columns if c.lower().startswith("uid")]
    df.drop(columns=uid_cols, inplace=True)

    # --------------------
    # BUILD UID PER ROW
    # --------------------

    def build_uid(row):
        state_key = (
            str(row["state"])
            .lower()
            .replace(" ", "")
            .replace("&", "")
        )

        if state_key not in state_map:
            raise KeyError(f"Unknown state: {row['state']}")

        state_code = state_map[state_key]

        return (
            state_code
            + YEAR
            + ELECTION_TYPE
            + str(int(row["no"])).zfill(2)
        )

    df["UID"] = df.apply(build_uid, axis=1)

    # ---- SAVE ----
    df.to_csv(csv_path, index=False)
