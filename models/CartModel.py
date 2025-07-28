from pydantic import BaseModel


class Cart(BaseModel):
    total: float
    bonus: int
