from pydantic import BaseModel


class Subscriber(BaseModel):
    email: str
