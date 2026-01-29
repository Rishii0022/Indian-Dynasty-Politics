import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
subs_key = os.getenv("OpenAI")
client = OpenAI(api_key=subs_key)

#error_file = client.files.content("error_file_id")

error_file = client.files.content("file-FgBXn7A51TQEoG4Rz1bRaX")
print(error_file.text)
