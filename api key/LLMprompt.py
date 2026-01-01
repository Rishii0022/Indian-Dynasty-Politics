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
You must exhaustively identify and include all publicly known direct and extended family members (including parents, siblings, grandparents, aunts, uncles, cousins, and in-laws) of the candidate who have held or contested any political office. Do not stop after listing one relative.
Before responding, internally verify that no other qualifying relatives are omitted.
use a web search before returning results
If any detail (years held, constituency, district, or state) is not publicly available, use “Unknown” instead of omitting the relative.
If none of the candidates direct or extended family members have held any political role, output exactly:
No family
Add all URL citations/sources so the user can verify the information provided.

Output Structure:
Relation - Relative Name — Political role/position - {Years held} — {[constituency name, district name, State name](if applicable / if known)}
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

# print(response.choices[0].message.content)
print(response.output_text)
print(json.dumps(response.model_dump(), indent=2))

# for item in response.output:
#     if item.type == "web_search_call":
#         print(item.action.sources)

