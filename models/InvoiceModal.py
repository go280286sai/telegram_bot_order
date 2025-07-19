from pydantic import BaseModel


class Invoice(BaseModel):
    body: str
