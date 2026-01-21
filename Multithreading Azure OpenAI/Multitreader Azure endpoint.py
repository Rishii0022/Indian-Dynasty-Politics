import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
from StructuredOutputNano import RelativesnSource
from batch_prompts_template import input1, tools1

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

response = client.responses.create(
    model=deployment,
    input = input1,
    tools = tools1
)

raw_text = response.output_text
parsed_json = json.loads(raw_text)
validated_output = RelativesnSource(**parsed_json)

print(validated_output.model_dump_json(indent=4))

# To measure the total tokens used(input/output)
# print(response.output_text)
# print(json.dumps(response.model_dump(), indent=2))

