from pydantic import BaseModel


class Template(BaseModel):
    header: str
    title: str
    body: str
