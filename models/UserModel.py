from pydantic import BaseModel


class User(BaseModel):
    """
    User model
    """
    username: str
    password: str
    email: str
    phone: str


class UpdateUser(BaseModel):
    """
    Update user model
    """
    idx: int
    password: str


class Login(BaseModel):
    """
    Login model
    """
    username: str
    password: str
