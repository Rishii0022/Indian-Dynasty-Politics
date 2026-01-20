import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
subs_key = os.getenv("OpenAI")
client = OpenAI(api_key=subs_key)


# file=open(r"JSONL file name local system", "rb")

batch_input_file = client.files.create(
    file=open(r"C:\Users\Rishi\Desktop\final dashboard\input_jsonl_batch\batch_input_telangana.jsonl", "rb"),
    purpose="batch"
)

print(batch_input_file)