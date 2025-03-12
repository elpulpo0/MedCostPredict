from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from backend.modules.api.users.security import hash_password
from backend.modules.db.preparation.users.create_db import User


from backend.modules.api.users.models import UserCreate, UserResponse, Token
from backend.modules.api.users.functions import (
    get_db,
    get_user_by_email,
    create_access_token,
    authenticate_user,
)

load_dotenv()  # Charge les variables d'environnement depuis .env

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Gestion de l'authentification avec OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users_router = APIRouter()


@users_router.post(
    "/users/",
    response_model=UserResponse,
    summary="Créer un nouvel utilisateur",
    description="Ajoute un nouvel utilisateur avec un email, "
    "un mot de passe haché et un rôle.",
    tags=["Utilisateurs"],
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = hash_password(user.password)
    db_user = User(
        full_name=user.full_name, email=user.email, hashed_password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@users_router.post(
    "/token",
    response_model=Token,
    summary="Connexion et génération d'un token JWT",
    description="Vérifie les informations de connexion et retourne "
    "un token d'authentification JWT si les identifiants sont corrects.",
    tags=["Utilisateurs"],
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@users_router.get(
    "/users/me",
    response_model=UserResponse,
    summary="Récupérer les informations de l'utilisateur connecté",
    description="Retourne les détails de l'utilisateur "
    "authentifié en utilisant son token.",
    tags=["Utilisateurs"],
)
def read_users_me(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


@users_router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Récupérer un utilisateur par son ID",
    description="Retourne les informations d'un utilisateur "
    "spécifique en fonction de son ID.",
    tags=["Utilisateurs"],
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


@users_router.get(
    "/users/",
    response_model=list[UserResponse],
    summary="Lister tous les utilisateurs",
    tags=["Utilisateurs"],
)
def get_all_users(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """Seuls les administrateurs peuvent voir tous les utilisateurs."""

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        requesting_user = get_user_by_email(email, db)

        if not requesting_user:
            raise HTTPException(
                status_code=401, detail="Utilisateur non trouvé."
            )

        if requesting_user.role != "admin":
            raise HTTPException(
                status_code=403,
                detail="Accès refusé : réservé aux administrateurs.",
            )

        return db.query(User).all()

    except JWTError:
        raise HTTPException(
            status_code=401, detail="Token invalide ou expiré."
        )


@users_router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un utilisateur",
    description="Supprime un utilisateur spécifique en fonction de son ID.",
    tags=["Utilisateurs"],
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    db.delete(user)
    db.commit()
    return {"message": "Utilisateur supprimé"}
