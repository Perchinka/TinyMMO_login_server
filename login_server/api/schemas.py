from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    password: str

class RegisterResponse(BaseModel):
    success: bool

class LoginRequest(BaseModel):
    username: str
    client_response: str

class LoginResponse(BaseModel):
    success: bool

