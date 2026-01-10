from pydantic import BaseModel, Field
from typing import Dict, List, Union, Optional

#extra="forbid"

class Relatives(BaseModel):
    Relation:str = Field(description = "Relation with the winning elected candidate")
    Name:str = Field(description = "Name of the relative")
    PoliticalRole:str = Field(description="Political role/position of the relative")
    YearsHeld:  Union[str, int] = Field(description="Years held")
    ConstituencyName: str = Field(description="Constituency name")
    DistrictName: str = Field(description="District name")
    StateName: str = Field(description="State name")

class Sources(BaseModel):
    url: str = Field(description = "url of the source")

class RelativesnSource(BaseModel):
    candidate_key: str = Field(description = "<candidate name>_<constituency>_,<district>_<election name>")
    family: List[Relatives]
    source: Optional[List[Sources]] = []