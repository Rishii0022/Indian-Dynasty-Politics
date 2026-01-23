import pandas as pd
import os
import re

# --------------------
# CONFIG
# --------------------

folder_path = r"C:\Users\Rishi\Desktop\final dashboard\Scrapped data\all PC elections"
ELECTION_TYPE = "PC"

# Goa, Daman and Diu held the same Lok Sabha elections as part of a single Union Territory from their liberation in 1961 until May 1987
# Mapped LokSabha seats containing state name Goa, Daman and Diu to DD(Daman and Diu)
# "Goa, Daman And Diu":"DD"


# Other older state names mapped back to current state territories
# Mapped LokSabha seats containing older state names to current state names
# Even though states were split and borders were redrawn I took the liberty of mapping the older state names to the current state as I wanted to showcase how dynasty politics effects a country, So I made the tradeoff of choosing vague current state names without understanding thr geo politics of the nation or the states be more a little bit more precise.
# You can think of it as the lousy work done by the British Empire and Sir Cyril Radcliffe in mapping the borders for India,Pakistan,Bangladesh.
# In all honesty the british empire had 5 weeks, I did it in 1 day(I probably did a better job).
# and even if i did do a lousy job as the British crown empire and Radcliffe, the only difference between my work and their work was that I won't be responsible directly/indirectly for the deaths of 200K - 2 Million people, needless to say all the wars/deaths that have happened or will happen, forever changing the region and its people.
# But hey! if we can look beyond these geo mapping issues I do think I did a decent job in portraying how deep rooted dynasty poitics in India truely is and how the idea of democracy is anyone can represent the people but how often times, only the people in places privilege rise to represent the people irrespective of their qualifications to do so.

#I know my project isn't perfect but if it was never about being perfect, it was about showcasing how we can leverage AI and new tools to solve real world problems, and the problem I tried to solve was showing how Dynasty Politics in India effect the nation from efficient growth.

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
