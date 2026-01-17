#Upload a batch file

import os
from openai import OpenAI

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

# Upload a file with a purpose of "batch"
file = client.files.create(
    file=open("test.jsonl", "rb"),
    purpose="batch",
    extra_body={"expires_after": {"seconds": 1209600, "anchor": "created_at"}}
    # Optional you can set to a number between 1209600-2592000. This is equivalent to 14-30 days
)

print(file.model_dump_json(indent=2))

print(f"File expiration: {datetime.fromtimestamp(file.expires_at) if file.expires_at is not None else 'Not set'}")

file_id = file.id
