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

response = client.responses.create(
    model=deployment,
    input =[
        {
            "role": "system",
            "content": """
            You are an AI assistant that helps people find information on political candidates elected in India based on a set of rules.
            Rules:
Output only direct and extended family members who meet the inclusion criteria from the user prompt 
You must exhaustively identify and include all publicly known direct and extended family members (including parents, siblings, spouse, grandparents, aunts, uncles, cousins, and in-laws) of the candidate who have held or contested any political office at any level. Do not stop after listing one relative.
Before responding, internally verify that no other qualifying relatives are omitted by cross-checking multiple independent credible sources.
Use a web search before returning results 
Add all URL citations/sources so the user can verify the information provided.

The JSON MUST follow this schema exactly:
{
  "candidate_key": <candidate name>_<constituency>_<district>_<election name>,
  "family": [
    {
      "Relation": "string",
      "Name": "string",
      "PoliticalRole": "string",
      "YearsHeld": "string"
      "ConstituencyName": "string",
      "DistrictName": "string",
      "StateName": "string"
    }
  ],
}
Rules:
- Use EXACT key names and capitalization as shown.
- Do NOT add extra keys.
- Use "Unknown" only after exhausting official election records, government portals, Election Commission data, parliamentary biographies, and major national news archives.
- If no family members qualify, return:
{
  "candidate_key": "<candidate name>_<constituency>_<district>_<election name>",
  "family": []
}
The response MUST start with '{' and end with '}'.
Think carefully step by step about what documents are needed to answer the query.
            """,
        },
        {
            "role": "user",
            "content":
                """
            Return only a list of direct and extended family members of elected political candidate Chittem Parnika Reddy who are involved in politics, The details of Chittem Parnika Reddy are added below as context.

Context:
State Name: Telangana 
Election Name: Telangana Assembly Elections 2023 
Constituency Name: Narayanpet 
District Name: Mahbubnagar
Father/husband name: VENKATESHWAR REDDY CHITTEM

"""
        }
    ],

    tools=[
        {
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "IN"
            }
        }
    ],
    # tool_choice= "required",
    include=["web_search_call.action.sources"],


    # max_completion_tokens=2500,
    temperature=0.55,
    top_p=1.0,

    # frequency_penalty=0.0,
    # presence_penalty=0.0,
)


# main working 2 lines below
print(response.output_text)
# print(json.dumps(response.model_dump(), indent=2))

from StructuredOutputRelatives import CandidateFamilyResponse

# raw_text = response.output_text
# parsed_json = json.loads(raw_text)
# validated_output = CandidateFamilyResponse(**parsed_json)
# validated_output2 = CitationResponse(**parsed_json)

# To get all Family Names
# for member in validated_output.family:
#     print(member)

#TO get all URLs
# for citation in validated_output2.citations:
#     print(citation)

#JSON formatted
# print(json.dumps(validated_output.model_dump(), indent=4))

#JSON directly
# print(validated_output.model_dump_json(indent=4))




