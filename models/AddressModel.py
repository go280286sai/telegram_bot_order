from pydantic import BaseModel


class Address(BaseModel):
    """
    Address model
    """
    name: str
