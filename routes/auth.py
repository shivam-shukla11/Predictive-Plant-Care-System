# routes/auth.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from logic.crud.users import (
    create_user,
    get_user_by_email,
    verify_password
)
from logic.model.user import UserCreate, UserPublic
from logic.core.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ---------------------------
# Login schema
# ---------------------------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------------------------
# Signup
# ---------------------------
@router.post("/signup", response_model=UserPublic)
def signup(user: UserCreate):
    try:
        new_user = create_user(user)

        return UserPublic(
            id=new_user.id,
            email=new_user.email,
            name=new_user.name,
            created_at=new_user.created_at
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ---------------------------
# Login
# ---------------------------
@router.post("/login")
def login(data: LoginRequest):
    user = get_user_by_email(data.email)

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(
        data={"sub": user.id, "email": user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }