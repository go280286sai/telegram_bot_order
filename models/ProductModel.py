from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    price: float
    amount: int
    service: int
