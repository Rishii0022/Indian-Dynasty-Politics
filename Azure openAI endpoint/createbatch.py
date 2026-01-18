# Submit a batch job with the file
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import json

load_dotenv()

subscription_key = os.getenv("AZURE_OPENAI_API_KEY")



endpoint = "https://apitest-resource.openai.azure.com/"
model_name = "gpt-4.1"
deployment = "gpt-4.1"

api_version = "2025-03-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)
batch_response = client.batches.create(
    input_file_id="file-8056877ef4aa4181875e1fc3f9c3a535",
    endpoint="/chat/responses", # While passing this parameter is required, the system will read your input file to determine if the chat completions or responses API is needed.
    completion_window="24h",
)


# Save batch ID for later use
batch_id = batch_response.id

print(batch_response.model_dump_json(indent=2))