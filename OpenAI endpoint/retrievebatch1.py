import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
subs_key = os.getenv("OpenAI")
client = OpenAI(api_key=subs_key)



# file_response = client.files.content("output_file_id")

file_response = client.files.content("file-4duqffBHe3aS97HGRCrcTy")
print(file_response.text)

#Opening the retrieved file and creating a new file on your local system

# with open("your_jsonl_file_location", "w", encoding="utf-8") as f:

with open(r"C:\Users\Rishi\Desktop\final dashboard\output_jsonl_batch\batch_output_telangana.jsonl", "w", encoding="utf-8") as f:
    f.write(file_response.text)


