from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# -------------------------
# Shared base
# -------------------------
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


# -------------------------
# Signup payload
# -------------------------
class UserCreate(UserBase):
    password: str


# -------------------------
# Login payload
# -------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -------------------------
# Stored in DB
# -------------------------
class UserInDB(UserBase):
    id: str
    hashed_password: str
    created_at: datetime


# -------------------------
# Sent to frontend
# -------------------------
class UserPublic(UserBase):
    id: str
    created_at: datetime
