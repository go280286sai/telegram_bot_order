from pydantic import BaseModel


class Transaction(BaseModel):
    transaction: str
    cardTotal: float
