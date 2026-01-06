from pydantic import BaseModel

class RequestCreate(BaseModel):
    name: str
    email: str
    title: str
    description: str

class RequestOut(RequestCreate):
    id: int
    status: str
