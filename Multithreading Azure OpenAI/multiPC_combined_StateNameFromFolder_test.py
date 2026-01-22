import csv
import json
import time
import os
from copy import deepcopy
from openai import AzureOpenAI
from dotenv import load_dotenv
from itertools import cycle
from batch_promptsPC_template import input1, tools1
from StructuredOutputNano import RelativesnSource

# ======================
# CONSTANTS
# ======================

Missing = "unknown"
YEAR = "2024"

INPUT_FOLDER = r"C:\Users\Rishi\Desktop\final dashboard\Scrapped data\PC split recent"
OUTPUT_FILE = r"C:\Users\Rishi\Desktop\final dashboard\outputPC_jsonl_batch\sync_output_LokSabha2024.jsonl"

# ======================

load_dotenv()

clients = [
    {
        "client": AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY3"),
            azure_endpoint="https://rishi-mkmva6p5-swedencentral.cognitiveservices.azure.com/",
            api_version="2025-03-01-preview"
        ),
        "deployment": "gpt-4.1"
    },
    {
        "client": AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY4"),
            azure_endpoint="https://rishi-mkmva6p5-swedencentral.cognitiveservices.azure.com/",
            api_version="2025-03-01-preview"
        ),
        "deployment": "gpt-4.1-2"
    },
    {
        "client": AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY1"),
            azure_endpoint="https://apitest-resource.openai.azure.com/",
            api_version="2025-03-01-preview"
        ),
        "deployment": "gpt-4.1"
    },
    {
        "client": AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY2"),
            azure_endpoint="https://apitest-resource.openai.azure.com/",
            api_version="2025-03-01-preview"
        ),
        "deployment": "gpt-4.1-2"
    }
]

client_cycle = cycle(clients)

# ======================
# HELPERS
# ======================

def clean_state_name(filename):
    return os.path.splitext(filename)[0].strip()


def build_prompt(row, STATE_NAME, ELECTION_NAME):
    prompt = deepcopy(input1)

    prompt[1]["content"] = prompt[1]["content"].format(
        candidate_name=row["winning candidate"].strip(),
        uid=row["UID"].strip(),
        state=STATE_NAME,
        election=ELECTION_NAME,
        district=row["pc name"].strip(),
        father_name=row["father/husband name"].strip()
    )

    return prompt


# ======================
# MAIN LOOP
# ======================

with open(OUTPUT_FILE, "a", encoding="utf-8") as outfile:

    for file in os.listdir(INPUT_FOLDER):

        if not file.lower().endswith(".csv"):
            continue

        CSV_FILE = os.path.join(INPUT_FOLDER, file)

        STATE_NAME = clean_state_name(file)
        ELECTION_NAME = f"{STATE_NAME} Lok Sabha Elections {YEAR}"

        print(f"\nProcessing: {STATE_NAME}")

        with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:

            reader = csv.DictReader(csvfile)

            for index, row in enumerate(reader, start=1):

                try:
                    prompt = build_prompt(row, STATE_NAME, ELECTION_NAME)

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

                    print(f"✅ {STATE_NAME} | {index} | {row['winning candidate']}")

                except Exception as e:
                    print("ERROR:", repr(e))

                    outfile.write(
                        json.dumps({
                            "UID": row.get("UID"),
                            "error": repr(e)
                        }) + "\n"
                    )

                time.sleep(2.2)
