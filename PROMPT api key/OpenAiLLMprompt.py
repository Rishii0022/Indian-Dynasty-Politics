import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from StructuredOutputFinal import RelativesnSource


load_dotenv()

subs_key = os.getenv("OpenAI")

client = OpenAI(api_key=subs_key)

response = client.responses.parse(
    model="gpt-5-nano",
    input =[
        {
            "role": "system",
            "content": """content": "You are an AI assistant that helps people find information on political candidates elected in India based on a set of rules. Rules: Output only direct and extended family members who meet the inclusion criteria from the user prompt. You must exhaustively identify and include all publicly known direct and extended family members (including parents, siblings, spouse, grandparents, aunts, uncles, cousins, and in-laws) of the candidate who have held or contested any political office at any level. Do not stop after listing one relative. Before responding, internally verify that no other qualifying relatives are omitted by cross-checking multiple independent credible sources. Use a web search before returning results. Add all URL citations/sources so the user can verify the information provided. The JSON MUST follow the provided schema exactly.Use EXACT key names and capitalization.Do NOT add extra keys.  Use Unknown only after exhausting official election records, government portals, Election Commission data, parliamentary biographies, and major national news archives. If no family members qualify, return an empty family array and sources array. Think carefully step by step about what documents are needed to answer the query.""",
        },
        {
            "role": "user",
            "content":"""Return only a list of direct and extended family members of elected political candidate Chikkudu Vamshi Krishna who are involved in politics, The details of Chikkudu Vamshi Krishna are added below as context. Context: State Name: Telangana, Election Name: Telangana Assembly Elections 2023, Constituency Name: Achampet, District Name: Mahbubnagar, Father/husband name:  CHINNA BALAIAH."""
        }
    ],
    tools=[
        {
            "type": "web_search",
            "user_location": {
                "type": "approximate",
                "country": "IN"
            }
        }
    ],
    text_format=RelativesnSource,
    top_p=1.0,
)

print(response.output_parsed)
print(json.dumps(response.model_dump(), indent=2))


