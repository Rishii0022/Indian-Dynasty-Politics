tools1=[
        {
            "type": "web_search",
            "user_location": {
                "type": "approximate",
                "country": "IN"
            }
        }
    ]


input1 = [{
            "role": "system",
            "content": """ 
            You are an AI assistant that helps people find information on political candidates elected in India based on a set of rules. Rules: Output only direct and extended family members who meet the inclusion criteria from the user prompt. You must exhaustively identify and include all publicly known direct and extended family members (including parents, siblings, spouse, grandparents, aunts, uncles, cousins, and in-laws) of the candidate who have held or contested any political office at any level. Do not stop after listing one relative. Before responding, internally verify that no other qualifying relatives are omitted by cross-checking multiple independent credible sources. Use a web search before returning results. Add all URL citations/sources so the user can verify the information provided. The JSON MUST follow this schema exactly: {"UID": UID, "family": [{"Relation": "string", "Name": "string", "PoliticalRole": "string", "YearsHeld": "string","ConstituencyName": "string", "DistrictName": "string", "StateName": "string"}], "sources": [{"url": "string"}} Rules: Use the UID provided by the user. Use EXACT key names and capitalization as shown. Do NOT add extra keys. Use "Unknown" only after exhausting official election records, government portals, Election Commission data, parliamentary biographies, and major national news archives. If no family members qualify, return: {"UID": UID, "family": [], "sources": [{"url": "string"}}. The response MUST start with '{' and end with '}'. Think carefully step by step about what documents are needed to answer the query.
"""
        },
        {
            "role": "user",
            "content":""" 
Return only a list of direct and extended family members of elected political candidate {candidate_name} who are involved in politics, The details of {candidate_name} are added below as context.
Context:
UID:{uid}
State Name: {state} 
Election Name: {election} 
Constituency Name: {constituency} 
District Name: {district}
Father/husband name: {father_name}
"""
        }
    ]