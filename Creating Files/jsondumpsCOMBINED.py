import json
import csv
import os
import glob
import re

# ====== FOLDERS ======

# input files from folder
input_folder = r"C:\Users\Rishi\Desktop\final dashboard\outputAC_jsonl_batch"

# output files from folder
family_folder = r"C:\Users\Rishi\Desktop\final dashboard\Final parsed tables\family tables(AC recent)"
sources_folder = r"C:\Users\Rishi\Desktop\final dashboard\Final parsed tables\Sources tables(AC recent)"
error_folder = r"C:\Users\Rishi\Desktop\final dashboard\prompt errors\AC recent errors"
log_folder = r"C:\Users\Rishi\Desktop\final dashboard\log data tables\AC recent logs"

# ====== HEADERS ======
family_fields = [
    "FamilyID", "UID", "Relation", "Name", "PoliticalRole",
    "YearsHeld", "ConstituencyName", "DistrictName", "StateName"
]

sources_fields = ["SourcesID", "UID", "url"]

# ====== FIND INPUT FILES ======
input_files = sorted(glob.glob(os.path.join(input_folder, "sync_output_*.jsonl")))

def normalize(text):
    return re.sub(r"[^a-z]", "", text.lower())

for input_path in input_files:

    filename = os.path.basename(input_path)

    # ---------- EXTRACT STATE NAME ----------
    state_raw = filename.replace("sync_output_", "").replace(".jsonl", "")

    # ---------- OUTPUT FILES ----------

    #Change names according to requirements

    family_csv  = os.path.join(family_folder,  f"{state_raw}AC_family_recent.csv")
    sources_csv = os.path.join(sources_folder, f"{state_raw}AC_sources_recent.csv")
    error_jsonl = os.path.join(error_folder,   f"{state_raw}AC_errors_recent.jsonl")
    log_file    = os.path.join(log_folder,     f"{state_raw}AC_logs_recent.txt")

    family_id = 1
    sources_id = 1
    line_no = 0

    with open(input_path, "r", encoding="utf-8") as infile, \
         open(family_csv, "w", newline="", encoding="utf-8") as fam_out, \
         open(sources_csv, "w", newline="", encoding="utf-8") as src_out, \
         open(error_jsonl, "w", encoding="utf-8") as err_out, \
         open(log_file, "w", encoding="utf-8") as log:

        family_writer = csv.DictWriter(fam_out, fieldnames=family_fields)
        sources_writer = csv.DictWriter(src_out, fieldnames=sources_fields)

        family_writer.writeheader()
        sources_writer.writeheader()

        for line in infile:
            line_no += 1
            raw_line = line.strip()

            if not raw_line:
                continue

            # ---------- JSON PARSING ----------
            try:
                data = json.loads(raw_line)
            except Exception as e:
                log.write(f"[LINE {line_no}] JSON parse failed: {e}\n")
                continue

            uid = data.get("UID", "")

            # ---------- EXISTING ERROR ----------
            if "error" in data:
                err_out.write(raw_line + "\n")
                log.write(f"[LINE {line_no}] Existing error preserved | UID={uid}\n")
                continue

            # ---------- FAMILY ----------
            family_array = data.get("family", [])

            if family_array:
                for member in family_array:
                    family_writer.writerow({
                        "FamilyID": family_id,
                        "UID": uid,
                        "Relation": member.get("Relation", ""),
                        "Name": member.get("Name", ""),
                        "PoliticalRole": member.get("PoliticalRole", ""),
                        "YearsHeld": member.get("YearsHeld", ""),
                        "ConstituencyName": member.get("ConstituencyName", ""),
                        "DistrictName": member.get("DistrictName", ""),
                        "StateName": member.get("StateName", "")
                    })
                    family_id += 1
            else:
                family_writer.writerow({
                    "FamilyID": family_id,
                    "UID": uid,
                    "Relation": "",
                    "Name": "",
                    "PoliticalRole": "",
                    "YearsHeld": "",
                    "ConstituencyName": "",
                    "DistrictName": "",
                    "StateName": ""
                })
                family_id += 1

            # ---------- SOURCES ----------
            for src in data.get("sources", []):
                sources_writer.writerow({
                    "SourcesID": sources_id,
                    "UID": uid,
                    "url": src.get("url", "")
                })
                sources_id += 1

            # ---------- PER-LINE LOG ----------
            log.write(
                f"[LINE {line_no}] UID={uid} | "
                f"family_rows={len(family_array) if family_array else 1} | "
                f"sources_rows={len(data.get('sources', []))}\n"
            )

        # ---------- FINAL SUMMARY ----------
        log.write("\nPROCESSING COMPLETE\n")
        log.write(f"Total family rows: {family_id - 1}\n")
        log.write(f"Total source rows: {sources_id - 1}\n")
