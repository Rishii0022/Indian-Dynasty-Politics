import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
subs_key = os.getenv("OpenAI")
client = OpenAI(api_key=subs_key)


# client.batches.cancel("batch_id_from_create")

client.batches.cancel("batch_id_from_create")