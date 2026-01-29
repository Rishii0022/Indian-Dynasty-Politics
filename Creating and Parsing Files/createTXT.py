import os

file_path = r"C:\Users\Rishi\Desktop\final dashboard\log data tables\AC recent logs\GoaAC_logs_recent.txt"

os.makedirs(os.path.dirname(file_path), exist_ok=True)

open(file_path, "w", encoding="utf-8").close()
