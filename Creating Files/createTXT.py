import os

file_path = r"C:\Users\Rishi\Desktop\final dashboard\log data tables\PC recent logs\LokSabha2024_logs.txt"

os.makedirs(os.path.dirname(file_path), exist_ok=True)

open(file_path, "w", encoding="utf-8").close()
