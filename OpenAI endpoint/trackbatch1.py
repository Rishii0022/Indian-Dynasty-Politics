import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
subs_key = os.getenv("OpenAI")
client = OpenAI(api_key=subs_key)


# batch = client.batches.retrieve("batch_id_from_create")

batch = client.batches.retrieve("batch_696ef267bef881909be26e186d648b3a")
print(batch)