import pandas as pd
import glob
import os

# Input locations(*.csv remains same)
files = glob.glob(
    r"C:\Users\Rishi\Desktop\final dashboard - Copy\Scrapped data\PC split recent\*.csv"
)

df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

# Output locations
output_folder = r"C:\Users\Rishi\Desktop\final dashboard - Copy\new files 2026"
output_file = "states_2024_pc.csv"

output_path = os.path.join(output_folder, output_file)

df.to_csv(output_path, index=False)
