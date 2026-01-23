import csv
import json
import time
import os
import re
import sys
from copy import deepcopy
from openai import AzureOpenAI
from dotenv import load_dotenv
from itertools import cycle

sys.path.append(
    r"C:\Users\Rishi\Desktop\final dashboard\Multithreading Azure OpenAI"
)

from batch_promptsPC_template import input1, tools1
from StructuredOutputSyncPC import RelativesnSource

INPUT_FILE = r"C:\Users\Rishi\Desktop\final dashboard\Scrapped data\all PC elections\states_1980_pc.csv"
OUTPUT_FILE = r"C:\Users\Rishi\Desktop\final dashboard\outputPC_jsonl_batch\sync_output_LokSabha1980.jsonl"

load_dotenv()

clients = [
    {
        "client": AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY5"),
            azure_endpoint="https://cbiti-mkq62dbs-swedencentral.services.ai.azure.com/",
            api_version="2025-03-01-preview"
        ),
        "deployment": "gpt-4.1"
    },
    {
        "client": AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY6"),
            azure_endpoint="https://cbiti-mkq62dbs-swedencentral.services.ai.azure.com/",
            api_version="2025-03-01-preview"
        ),
        "deployment": "gpt-4.1-2"
    }
    # {
    #     "client": AzureOpenAI(
    #         api_key=os.getenv("AZURE_OPENAI_API_KEY3"),
    #         azure_endpoint="https://rishi-mkmva6p5-swedencentral.cognitiveservices.azure.com/",
    #         api_version="2025-03-01-preview"
    #     ),
    #     "deployment": "gpt-4.1"
    # },
    # {
    #     "client": AzureOpenAI(
    #         api_key=os.getenv("AZURE_OPENAI_API_KEY4"),
    #         azure_endpoint="https://rishi-mkmva6p5-swedencentral.cognitiveservices.azure.com/",
    #         api_version="2025-03-01-preview"
    #     ),
    #     "deployment": "gpt-4.1-2"
    # }
]

client_cycle = cycle(clients)

# Getting data from column names and adding it to the prompt

def extract_year_from_filename(filename: str) -> str:
    match = re.search(r"(18|19|20)\d{2}", filename)
    return match.group(0) if match else "Unknown"


def clean_state_name(filename: str) -> str:
    name = os.path.splitext(filename)[0]
    name = re.sub(r"(18|19|20)\d{2}", "", name)
    return name.replace("_", " ").strip()


def normalize_row(row: dict) -> dict:

    clean = {}
    for key, value in row.items():
        key = (
            key.replace("\ufeff", "")
               .replace("\u200b", "")
               .strip()
               .lower()
        )
        clean[key] = value.strip() if isinstance(value, str) else value
    return clean


def safe_get(row: dict, key: str, default=""):
    return row.get(key.lower(), default)


def build_prompt(row, STATE_NAME, YEAR):
    prompt = deepcopy(input1)

    prompt[1]["content"] = prompt[1]["content"].format(
        candidate_name=safe_get(row, "winning candidate"),
        uid=safe_get(row, "uid"),
        state=safe_get(row, "state"),
        year=YEAR,
        pc_name=safe_get(row, "pc name")
    )

    return prompt

file = os.path.basename(INPUT_FILE)

STATE_NAME = clean_state_name(file)
YEAR = extract_year_from_filename(file)

print(f"\nProcessing: {STATE_NAME} | {YEAR}")

with open(OUTPUT_FILE, "a", encoding="utf-8") as outfile:

    with open(INPUT_FILE, newline="", encoding="utf-8-sig") as csvfile:

        reader = csv.DictReader(csvfile)

        # For the input files headers
        # print("CSV HEADERS:", reader.fieldnames)

        for index, raw_row in enumerate(reader, start=1):

            row = normalize_row(raw_row)

            try:
                prompt = build_prompt(row, STATE_NAME, YEAR)

                # PRINT PROMPT BEING SENT
                # print("\n===== PROMPT SENT TO MODEL =====")
                # print(json.dumps(prompt, indent=2, ensure_ascii=False))
                # print("================================\n")

                cfg = next(client_cycle)

                response = cfg["client"].responses.create(
                    model=cfg["deployment"],
                    input=prompt,
                    tools=tools1
                )

                parsed = json.loads(response.output_text)
                validated = RelativesnSource(**parsed)

                outfile.write(
                    json.dumps(
                        validated.model_dump(),
                        ensure_ascii=False
                    ) + "\n"
                )

                print(
                    f"✅ {STATE_NAME} | {YEAR} | {index} | "
                    f"{safe_get(row, 'winning candidate')}"
                )

            except Exception as e:
                outfile.write(
                    json.dumps({
                        "UID": safe_get(row, "uid"),
                        "error": repr(e)
                    }) + "\n"
                )

                print("ERROR:", repr(e))

            time.sleep(2.2)
