import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
subs_key = os.getenv("OpenAI")
client = OpenAI(api_key=subs_key)


# batch_input_file_id = file_id_from_upload

batch_input_file_id = "file-D7F6MxVzMUyPLaBxd7VBJE"
batch = client.batches.create(
    input_file_id=batch_input_file_id,
    endpoint="/v1/responses",
    completion_window="24h",
    metadata={
        "description": "testbatch001"
    }
)

print(batch)
