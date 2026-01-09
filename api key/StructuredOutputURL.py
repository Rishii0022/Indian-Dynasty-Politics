from dataclasses import Field

from pydantic import BaseModel
from typing import List

class Citation(BaseModel):
    url: str
    title: str
    start_index: int
    end_index: int

class CitationResponse(BaseModel):
    candidate_key: str
    citations: List[Citation]
