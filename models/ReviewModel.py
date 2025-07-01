from typing import Optional

from pydantic import BaseModel


class Review(BaseModel):
    """
    ReviewModel
    """
    name: str
    text: str
    gender: int
