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


#test for batch api jsonl creator

# \nThe JSON MUST follow the provided schema exactly.\nUse EXACT key names and capitalization.\nDo NOT add extra keys.\nIf no family members qualify, return candidate_key and an empty family array.\nThe response MUST start with '{' and end with '}
#
#
# The JSON MUST follow this schema exactly:{"candidate_key": <candidate name>_<constituency>_<district>_<election name>,"family": [{"Relation": "string","Name": "string","PoliticalRole": "string","YearsHeld": "string","ConstituencyName": "string","DistrictName": "string","StateName": "string"}]


{
  "custom_id": "task-0",
  "method": "POST",
  "url": "/v1/responses",
  "body": {
    "model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME",
    "input": [
      {
        "role": "system",
        "content": "You are an AI assistant that helps people find information on political candidates elected in India based on a set of rules.\nRules:\nOutput only direct and extended family members who meet the inclusion criteria from the user prompt.\nYou must exhaustively identify and include all publicly known direct and extended family members (including parents, siblings, spouse, grandparents, aunts, uncles, cousins, and in-laws) of the candidate who have held or contested any political office at any level.\nUse a web search before returning results.\nAdd all URL citations/sources.\nThe JSON MUST follow the provided schema exactly.\nUse EXACT key names and capitalization.\nDo NOT add extra keys.\nIf no family members qualify, return candidate_key and an empty family array.\nThe response MUST start with '{' and end with '}'."
      },
      {
        "role": "user",
        "content": "Return only a list of direct and extended family members of elected political candidate Chittem Parnika Reddy who are involved in politics.\n\nContext:\nState Name: Telangana\nElection Name: Telangana Assembly Elections 2023\nConstituency Name: Narayanpet\nDistrict Name: Mahbubnagar\nFather/husband name: VENKATESHWAR REDDY CHITTEM"
      }
    ],
    "tools": [
      {
        "type": "web_search_preview",
        "user_location": {
          "type": "approximate",
          "country": "IN"
        }
      }
    ],
    "include": ["web_search_call.action.sources"],
    "text": {
      "format": {
        "type": "json_schema",
        "name": "CandidateFamilyResponse",
        "schema": {
          "type": "object",
          "properties": {
            "family": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "Relation": { "type": "string" },
                  "Name": { "type": "string" },
                  "PoliticalRole": { "type": "string" },
                  "YearsHeld": { "type":"string" },
                  "ConstituencyName": { "type": "string" },
                  "DistrictName": { "type": "string" },
                  "StateName": { "type": "string" }
                },
                "required": [
                  "Relation",
                  "Name",
                  "PoliticalRole",
                  "YearsHeld",
                  "ConstituencyName",
                  "DistrictName",
                  "StateName"
                ],
                "additionalProperties": false
              }
            },
            "sources": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "url": { "type": "string" }
                },
                "required": ["url"],
                "additionalProperties": false
              }
            }
          },
          "required": ["family", "sources"],
          "additionalProperties": false
        },
        "strict": true
      }
    }
  }
}


{"custom_id": "task-0", "method": "POST", "url": "/v1/chat/completions",
 "body": {"model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME",
          "messages": [{"role": "system", "content": "Extract the event information."},
                       {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."}],
          "response_format": {"type": "json_schema", "json_schema": {"name": "CalendarEventResponse", "strict": true,
          "schema": {"type": "object", "properties": {"name": {"type": "string"}, "date": {"type": "string"}, "participants":
        {"type": "array", "items": {"type": "string"}}}, "required": ["name", "date", "participants"], "additionalProperties": false}}}}}



#unchanged straight for chatgpt

{
  "custom_id": "task-0",
  "method": "POST",
  "url": "/v1/responses",
  "body": {
    "model": "REPLACE-WITH-MODEL-DEPLOYMENT-NAME",
    "input": [
      {
        "role": "system",
        "content": "You are an AI assistant that helps people find information on political candidates elected in India based on a set of rules.\nRules:\nOutput only direct and extended family members who meet the inclusion criteria from the user prompt.\nYou must exhaustively identify and include all publicly known direct and extended family members (including parents, siblings, spouse, grandparents, aunts, uncles, cousins, and in-laws) of the candidate who have held or contested any political office at any level.\nUse a web search before returning results.\nAdd all URL citations/sources.\nThe JSON MUST follow the provided schema exactly.\nUse EXACT key names and capitalization.\nDo NOT add extra keys.\nIf no family members qualify, return candidate_key and an empty family array.\nThe response MUST start with '{' and end with '}'."
      },
      {
        "role": "user",
        "content": "Return only a list of direct and extended family members of elected political candidate Chittem Parnika Reddy who are involved in politics.\n\nContext:\nState Name: Telangana\nElection Name: Telangana Assembly Elections 2023\nConstituency Name: Narayanpet\nDistrict Name: Mahbubnagar\nFather/husband name: VENKATESHWAR REDDY CHITTEM"
      }
    ],
    "tools": [
      {
        "type": "web_search_preview",
        "user_location": {
          "type": "approximate",
          "country": "IN"
        }
      }
    ],
    "include": ["web_search_call.action.sources"],
    "text": {
      "format": {
        "type": "json_schema",
        "name": "CandidateFamilyResponse",
        "schema": {
          "type": "object",
          "properties": {
            "candidate_key": { "type": "string" },
            "family": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "Relation": { "type": "string" },
                  "Name": { "type": "string" },
                  "PoliticalRole": { "type": "string" },
                  "YearsHeld": { "type": "string" },
                  "ConstituencyName": { "type": "string" },
                  "DistrictName": { "type": "string" },
                  "StateName": { "type": "string" }
                },
                "required": [
                  "Relation",
                  "Name",
                  "PoliticalRole",
                  "YearsHeld",
                  "ConstituencyName",
                  "DistrictName",
                  "StateName"
                ],
                "additionalProperties": false
              }
            },
            "source": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "url": { "type": "string" }
                },
                "required": ["url"],
                "additionalProperties": false
              }
            }
          },
          "required": ["candidate_key", "family"],
          "additionalProperties": false
        },
        "strict": true
      }
    }
  }
}

#iteration final 2833 characters

{"custom_id": "task-1", "method": "POST", "url": "/v1/responses", "body": {"model": "gpt-4.1", "input": [{"role": "system", "content": "You are an AI assistant that helps people find information on political candidates elected in India based on a set of rules. Rules: Output only direct and extended family members who meet the inclusion criteria from the user prompt. You must exhaustively identify and include all publicly known direct and extended family members (including parents, siblings, spouse, grandparents, aunts, uncles, cousins, and in-laws) of the candidate who have held or contested any political office at any level. Do not stop after listing one relative. Before responding, internally verify that no other qualifying relatives are omitted by cross-checking multiple independent credible sources. Use a web search before returning results. Add all URL citations/sources so the user can verify the information provided. The JSON MUST follow the provided schema exactly.Use EXACT key names and capitalization.Do NOT add extra keys.  Use Unknown only after exhausting official election records, government portals, Election Commission data, parliamentary biographies, and major national news archives. If no family members qualify, return an empty family array and source array.The response MUST start with '{' and end with '}'. Think carefully step by step about what documents are needed to answer the query."}, {"role": "user", "content": "Return only a list of direct and extended family members of elected political candidate Chittem Parnika Reddy who are involved in politics, The details of Chittem Parnika Reddy are added below as context. Context: State Name: Telangana, Election Name: Telangana Assembly Elections 2023, Constituency Name: Narayanpet, District Name: Mahbubnagar, Father/husband name: VENKATESHWAR REDDY CHITTEM"}],"tools": [{ "type": "web_search_preview", "user_location": {"type": "approximate","country": "IN"}}], "include": ["web_search_call.action.sources"], "text": {"format": {"type": "json_schema", "name": "CandidateFamilyResponse", "schema": {"type": "object", "properties": {"family": {"type": "array","items": {"type": "object", "properties": {"Relation": { "type": "string" }, "Name": { "type": "string" }, "PoliticalRole": { "type": "string" }, "YearsHeld": { "type":"string" },"ConstituencyName": { "type": "string" }, "DistrictName": { "type": "string" }, "StateName": { "type": "string" }}, "required": ["Relation", "Name", "PoliticalRole", "YearsHeld", "ConstituencyName", "DistrictName", "StateName"],"additionalProperties": false}}, "sources": {"type": "array", "items": {"type": "object", "properties": {"url": { "type": "string" }},"required": ["url"], "additionalProperties": false}}}, "required": ["family", "sources"], "additionalProperties": false},"strict": true}}}}

#changed stuff
# chnaged source to sources for entire prompt


# removed
# "include": ["web_search_call.action.sources"],


#openai all sources

family_output = response.output_parsed

# searched URLs
searched_urls = [
    s.model_dump() for s in response.output[0].action.sources
]

# citation annotations
citations = [
    c.model_dump() for c in response.output[1].content[0].annotations
]

# ---------------- FINAL MERGE ----------------

final_output = {
    "family": [r.model_dump() for r in family_output.family],
    "sources": searched_urls,
    "citations": citations
}

print(json.dumps(final_output, indent=2))

# class Citation(BaseModel):
#     type: str
#     url: str = Field(description = "url of the source")
#     title: Optional[str] = Field(description = "Title of the source")
#     start_index: Optional[int] = Field(description = "Start index of the source")
#     end_index: Optional[int] = Field(description = "End index of the source")

include=["web_search_call.action.sources"],

