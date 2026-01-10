from dataclasses import Field

from pydantic import BaseModel
from typing import List

class Source(BaseModel):
    url: str = Field(description="url of the source")
    title: str = Field(description="Title of the source")
    start_index: int = Field(description="start index of the citation")
    end_index: int = Field(description="end index of the source")

class SourceResponse(BaseModel):
    candidate_key: str
    Sources: List[Source]
