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
    password: str


class Login(BaseModel):
    """
    Login model
    """
    username: str
    password: str


class UpdateUsers(BaseModel):
    username: str
    email: str
    phone: str
    comments: str
    first_name: str
    last_name: str


class AddName(BaseModel):
    first_name: str
    last_name: str
