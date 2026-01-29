# Remove duplicates based on all columns, drop column one

import pandas as pd

df = pd.read_csv(r"csv_path")

df = df.drop_duplicates()

# Remove duplicates based on a specific column
df = df.drop_duplicates(subset=['AC Name'])

df = df.drop(df.columns[0], axis=1)  # axis=1 means column

# Save back to CSV
df.to_csv(r"csv_path", index=False)








