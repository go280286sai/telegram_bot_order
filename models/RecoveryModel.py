from pydantic import BaseModel


class Recovery(BaseModel):
    username: str
    email: str
