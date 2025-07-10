from pydantic import BaseModel


class Setting(BaseModel):
    name: str
    value: str
