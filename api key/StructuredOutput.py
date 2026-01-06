from pydantic import BaseModel, Field
from typing import Dict, List


class Relatives(BaseModel, extra="forbid"):
    Relation:str = Field(description = "Relation with the relative")
    Name:str = Field(description = "Name of the relative")
    PoliticalRole:str = Field(description="Political role/position")
    YearsHeld: int = Field(description="Years held")
    ConstituencyName: str = Field(description="Constituency name")
    DistrictName: str = Field(description="District name")
    StateName: str = Field(description="State name")

class CandidateFamilyResponse(BaseModel):
    candidate_key: str
    family: List[Relatives]









