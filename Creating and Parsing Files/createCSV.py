import os

file_path = r"C:\Users\Rishi\Desktop\final dashboard\Final parsed tables\Sources tables(AC recent)\NagalandAC_sources_recent.csv"

os.makedirs(os.path.dirname(file_path), exist_ok=True)

open(file_path, "w").close()
