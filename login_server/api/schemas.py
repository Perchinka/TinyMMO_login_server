from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str


class RegisterResponse(BaseModel):
    success: bool


class ChallengeRequest(BaseModel):
    username: str


class ChallengeResponse(BaseModel):
    nonce: str
    salt: str


class AuthRequest(BaseModel):
    username: str
    encrypted_challenge: str


class AuthResponse(BaseModel):
    success: bool
