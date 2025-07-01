from pydantic import BaseModel


class Post(BaseModel):
    """
    Post model
    """
    name: str
