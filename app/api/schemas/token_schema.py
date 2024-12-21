from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class UserCreateRequest(BaseModel):
    email: str
    username: str
    password: str

