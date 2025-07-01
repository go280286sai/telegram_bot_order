from pydantic import BaseModel


class City(BaseModel):
    """
    City model
    """
    name: str
