from pydantic import BaseModel

class LoginModel(BaseModel):
    login: str
    password: str
    symbol: str
    journal: str

class UserModel(BaseModel):
    expiration_date: float
    key: bytes