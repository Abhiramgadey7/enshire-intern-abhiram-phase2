from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    role: str = Field(default="user", description="Role can be 'user' or 'admin'")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Plaintext password")

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None