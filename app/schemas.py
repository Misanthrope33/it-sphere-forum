from pydantic import BaseModel

class PostCreate(BaseModel):
    author: str
    title: str
    content: str

class PostResponse(PostCreate):
    id: int

    class Config:
        from_attributes = True