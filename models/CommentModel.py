from pydantic import BaseModel


class Comment(BaseModel):
    body: str
