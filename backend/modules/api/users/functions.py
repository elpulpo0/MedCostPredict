from datetime import datetime, timedelta
from backend.modules.db.preparation.users.create_db import SessionLocal, User
from backend.modules.api.users.security import verify_password
from sqlalchemy.orm import Session
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables d'environnement depuis .env

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(email, db)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user
