from pydantic import BaseModel


class Carousel(BaseModel):
    """
    Carousel model
    """
    title: str
    description: str
    image: str
