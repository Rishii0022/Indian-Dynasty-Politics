import json
import csv

# ====== FILE PATHS ======

# Existing input files
input_jsonl = r"C:\Users\Rishi\Desktop\final dashboard\outputAC_jsonl_batch\sync_output_AndhraPradesh.jsonl"

# created output files
family_csv = r"C:\Users\Rishi\Desktop\final dashboard\Final parsed tables\family tables(AC recent)\AndhraPradeshAC_family_recent.csv"
sources_csv = r"C:\Users\Rishi\Desktop\final dashboard\Final parsed tables\Sources tables(AC recent)\AndhraPradeshAC_sources_recent.csv"
error_jsonl = r"C:\Users\Rishi\Desktop\final dashboard\prompt errors\AC recent errors\AndhraPradeshAC_errors_recent.jsonl"
log_file = r"C:\Users\Rishi\Desktop\final dashboard\log data tables\AC recent logs\AndhraPradeshAC_logs_recent.txt"

# ====== CSV HEADERS ======
family_fields = [
    "FamilyID", "UID", "Relation", "Name", "PoliticalRole",
    "YearsHeld", "ConstituencyName", "DistrictName", "StateName"
]

sources_fields = [
    "SourcesID", "UID", "url"
]

# ====== COUNTERS ======
family_id = 1
sources_id = 1
line_no = 0

# ====== OPEN FILES ======
with open(input_jsonl, "r", encoding="utf-8") as infile, \
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

        # ---------- EXISTING ERROR OBJECT ----------
        if "error" in data:
            err_out.write(raw_line + "\n")
            log.write(f"[LINE {line_no}] Existing error preserved | UID={uid}\n")
            continue

        # ---------- FAMILY TABLE ----------
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
            # empty family array → UID only, rest blank
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

        # ---------- SOURCES TABLE ----------
        for src in data.get("sources", []):
            sources_writer.writerow({
                "SourcesID": sources_id,
                "UID": uid,
                "url": src.get("url", "")
            })
            sources_id += 1

        log.write(
            f"[LINE {line_no}] UID={uid} | "
            f"family_rows={len(family_array) if family_array else 1} | "
            f"sources_rows={len(data.get('sources', []))}\n"
        )

    log.write("\nPROCESSING COMPLETE\n")
    log.write(f"Total family rows: {family_id - 1}\n")
    log.write(f"Total source rows: {sources_id - 1}\n")
