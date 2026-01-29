#make second row header

import pandas as pd

# Load CSV without treating the first row as header
df = pd.read_csv(r"C:\Users\Rishi\Desktop\scraping for indian politics\Haryana_2019_ac.csv", header=None)

# Drop the first row
df = df.iloc[1:]

# Save back to CSV
df.to_csv(r"C:\Users\Rishi\Desktop\scraping for indian politics\Haryana_2019_ac.csv", index=False, header=False)

print("First row deleted and CSV saved successfully!")

