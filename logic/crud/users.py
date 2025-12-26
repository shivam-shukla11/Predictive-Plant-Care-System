from datetime import datetime
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from passlib.context import CryptContext

from db import db
from logic.model.user import UserCreate, UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_collection = db["users"]

# Ensure unique email
users_collection.create_index("email", unique=True)


# ---------------------------
# Password helpers
# ---------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


# ---------------------------
# Create user
# ---------------------------
def create_user(user: UserCreate) -> UserInDB:
    now = datetime.utcnow()

    user_dict = {
        "email": user.email,
        "name": user.name,
        "hashed_password": hash_password(user.password),
        "created_at": now
    }

    try:
        result = users_collection.insert_one(user_dict)
    except DuplicateKeyError:
        raise ValueError("User with this email already exists")

    return UserInDB(
        id=str(result.inserted_id),
        email=user.email,
        name=user.name,
        hashed_password=user_dict["hashed_password"],
        created_at=now
    )


# ---------------------------
# Get user by email
# ---------------------------
def get_user_by_email(email: str) -> UserInDB | None:
    doc = users_collection.find_one({"email": email})

    if not doc:
        return None

    return UserInDB(
        id=str(doc["_id"]),
        email=doc["email"],
        name=doc.get("name"),
        hashed_password=doc["hashed_password"],
        created_at=doc["created_at"]
    )
