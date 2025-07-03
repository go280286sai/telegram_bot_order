from pydantic import BaseModel


class Pay(BaseModel):
    cardTotal: float
    cardNumber: str
    cardMonth: str
    cardYear: str
    cardKey: str
