from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    uid: str = Field(...)
    name: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)
    phone: Optional[str] = None
    photoURL: Optional[str] = None
    bio: Optional[str] = None
    onboardingComplete: bool = False
    createdAt: Optional[float] = None
    updatedAt: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "uid": "user123",
                "name": "John Doe",
                "username": "johndoe",
                "email": "johndoe@example.com",
                "phone": "+254700000000",
                "photoURL": "https://mega.nz/...",
                "bio": "Digital Creator",
                "onboardingComplete": False
            }
        }

class UpdateUserModel(BaseModel):
    name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    photoURL: Optional[str]
    bio: Optional[str]
    onboardingComplete: Optional[bool]
    updatedAt: Optional[float]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "bio": "Updated bio",
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
