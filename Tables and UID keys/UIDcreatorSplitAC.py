import pandas as pd
import os
import re

csv_path = r"C:\Users\Rishi\Desktop\final dashboard\ac recent"
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
    "Telangana":"TG"

}
state_map = {k.lower().replace(" ", ""): v for k, v in state_map.items()}

#Folder location
for file in os.listdir(r"C:\Users\Rishi\Desktop\final dashboard\ac recent"):
    if not file.lower().endswith(".csv"):
        continue

    csv_path = os.path.join(r"C:\Users\Rishi\Desktop\final dashboard\ac recent", file)
    filename = file.lower()

    # parse filename
    state_key = filename.split("_")[0].replace(" ", "")
    state_code = state_map[state_key]
    year = re.search(r"\d{4}", filename).group()
    election_type = "AC" if "_ac" in filename else "PC"

    # load csv
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(".", "", regex=False)
    )

    # <<< ADDED: explicitly resolve AC No column variations >>>
    ac_variants = {"ac no", "acno"}
    ac_no_column = next(
        (c for c in df.columns if c.replace(" ", "") in ac_variants),
        None
    )

    if ac_no_column is None:
        raise KeyError(f"AC No column not found in {csv_path}")

    uid_cols = [c for c in df.columns if c.lower().startswith("uid")]
    df.drop(columns=uid_cols, inplace=True)


    mask = df[ac_no_column].notna()

    # create UID
    df.loc[mask,"UID"] = (
        state_code
        + year
        + election_type
        + df.loc[mask,ac_no_column].astype(int).astype(str).str.zfill(2)
    )

    # overwrite same file
    df.to_csv(csv_path, index=False)
