from pydantic import BaseModel, Field

class Relatives(BaseModel):
    Relation:str = field("Relation with the relative")
    Name:str = field("Name of the relative")




