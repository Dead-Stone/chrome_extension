from pydantic import BaseModel

class User(BaseModel):
    user_id: str

class Paper(BaseModel):
    paper_id: str
    title: str
    abstract: str
    link: str

class Interaction(BaseModel):
    user_id: str
    paper_id: str
    interaction_type: str
