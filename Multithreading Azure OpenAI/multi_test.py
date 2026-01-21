import csv
import json
import time
import os
from copy import deepcopy
from openai import AzureOpenAI
from dotenv import load_dotenv
from itertools import cycle
from batch_prompts_template import input1, tools1
from StructuredOutputNano import RelativesnSource

# ======================
# MANUAL CONSTANT VALUES
# ======================

#change STATE NAME
STATE_NAME = "Himachal Pradesh"

#Change YEAR AND STATE NAME
ELECTION_NAME = "Himachal Pradesh Assembly Elections 2022"

CSV_FILE = r"C:\Users\Rishi\Desktop\final dashboard\Scrapped data\ac recent\HimachalPradesh_2022_ac.csv"
OUTPUT_FILE = r"C:\Users\Rishi\Desktop\final dashboard\output_jsonl_batch\sync_output_Himachal Pradesh.jsonl"

# ======================

load_dotenv()

clients = [
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
    },
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
    }
]

client_cycle = cycle(clients)


def build_prompt(row):
    prompt = deepcopy(input1)

    prompt[1]["content"] = prompt[1]["content"].format(
        candidate_name=row["winning candidate"].strip(),
        uid=row["UID"].strip(),
        state=STATE_NAME,
        election=ELECTION_NAME,
        constituency=row["ac name"].strip(),
        district=row["district"].strip(),
        father_name=row["father/husband name"].strip()
    )

    return prompt

def get_last_processed_uid(output_file):
    if not os.path.exists(output_file):
        return None

    with open(output_file, "r", encoding="utf-8") as f:
        for line in f:
            pass

    try:
        return json.loads(line).get("UID")
    except Exception:
        return None



with open(CSV_FILE, newline="", encoding="utf-8") as csvfile, \
     open(OUTPUT_FILE, "a", encoding="utf-8") as outfile:

    reader = csv.DictReader(csvfile)
    last_uid = get_last_processed_uid(OUTPUT_FILE)
    skip = True if last_uid else False

    for index, row in enumerate(reader, start=1):

        if skip:
            if row["UID"] == last_uid:
                skip = False
            continue

        try:
            prompt = build_prompt(row)

            cfg = next(client_cycle)

            response = cfg["client"].responses.create(
                model=cfg["deployment"],
                input=prompt,
                tools=tools1
            )

            parsed = json.loads(response.output_text)
            validated = RelativesnSource(**parsed)

            outfile.write(
                json.dumps(validated.model_dump(), ensure_ascii=False) + "\n"
            )

            print(f"✅ {index} | {row['winning candidate']}")

        except Exception as e:
            print("ERROR:", repr(e))

            outfile.write(
                json.dumps({
                    "UID": row.get("UID"),
                    "error": repr(e)
                }) + "\n"
            )

        time.sleep(2.2)  # prevents 429


