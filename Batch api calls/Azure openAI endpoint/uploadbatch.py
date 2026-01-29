#Upload a batch file

import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import json

load_dotenv()

subscription_key = os.getenv("AZURE_OPENAI_API_KEY")



endpoint = "API_endpoint"
model_name = "API_model"
deployment = "API_model"

api_version = "API_version"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)


subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
client = AzureOpenAI(
    base_url="API_endpoint",
    api_key=subscription_key,
    api_version = "API_version"
)

# Upload a file with a purpose of "batch"
file = client.files.create(
    file=open(r"batch_input_jsonl", "rb"),
    purpose="batch",
    extra_body={"expires_after": {"seconds": 1209600, "anchor": "created_at"}}
    # 1209600 = 14 days
)

print(file.model_dump_json(indent=2))

print(f"File expiration: {datetime.fromtimestamp(file.expires_at) if file.expires_at is not None else 'Not set'}")

file_id = file.id
