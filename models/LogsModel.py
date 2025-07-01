from pydantic import BaseModel


class Logs(BaseModel):
    """
    Logs model
    """
    level: str
    name: str
    message: str
