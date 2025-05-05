from pydantic import BaseModel

class User(BaseModel):
    username: str
    password_hash: str

