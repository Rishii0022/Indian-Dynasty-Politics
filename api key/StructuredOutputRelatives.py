from pydantic import BaseModel, Field
from typing import Dict, List, Union

#extra="forbid"

class Relatives(BaseModel):
    Relation:str = Field(description = "Relation with the relative")
    Name:str = Field(description = "Name of the relative")
    PoliticalRole:str = Field(description="Political role/position")
    YearsHeld:  Union[str, int] = Field(description="Years held")
    ConstituencyName: str = Field(description="Constituency name")
    DistrictName: str = Field(description="District name")
    StateName: str = Field(description="State name")

class CandidateFamilyResponse(BaseModel):
    candidate_key: str = Field(description = "<candidate name>_<constituency>_,<district>_<election name>")
    family: List[Relatives]









