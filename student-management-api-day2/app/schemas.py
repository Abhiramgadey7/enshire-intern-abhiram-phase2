from pydantic import BaseModel, Field
from typing import List


# -----------------------
# User Schemas (Day 2)
# -----------------------

class UserCreate(BaseModel):
    email: str
    password: str
    role: str = "user"


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True


# -----------------------
# Student Schemas (Day 3)
# -----------------------

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=1, le=120)
    course: str = Field(..., min_length=2, max_length=100)


class StudentUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=1, le=120)
    course: str = Field(..., min_length=2, max_length=100)


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    course: str

    class Config:
        from_attributes = True


class StudentListResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: List[StudentResponse]