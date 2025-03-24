from datetime import datetime, timedelta
from backend.modules.db.preparation.users.create_db import SessionLocal, User
from backend.utils.security import anonymize, verify_password
from backend.utils.logger import setup_logger
from sqlalchemy.orm import Session
from jose import jwt
import os
from dotenv import load_dotenv

# Initialisation du logger
logger = setup_logger(log_name="api_users_functions")

# Charger les variables d'environnement
load_dotenv()

# Vérifier si la clé secrète est bien définie dans les variables d'environnement
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY est absent dans les variables d'environnement."
    )

ALGORITHM = "HS256"  # Algorithme de codage pour JWT


def get_db():
    """Retourne une session de base de données."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Crée un access token pour un utilisateur donné."""
    logger.info("Création du token d'accès...")

    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Token d'accès créé avec expiration à : {expire}")

    return encoded_jwt


def get_user_by_email(email: str, db: Session):
    # Effectuer la recherche dans la base de données avec l'email anonymisé
    user = db.query(User).filter(User.email == email).first()

    return user


def authenticate_user(db: Session, email: str, password: str):
    """Authentifie un utilisateur en vérifiant son email et son mot de passe."""
    logger.info("Authentification de l'utilisateur...")

    # Récupérer l'utilisateur en utilisant l'email
    user = get_user_by_email(email, db)

    # Vérifier si l'utilisateur existe et si le mot de passe est valide
    if not user:
        logger.info("Utilisateur non trouvé.")
        return False

    if not verify_password(password, user.password):
        logger.info("Mot de passe invalide.")
        return False

    logger.info(f"Utilisateur authentifié avec succès")
    return user
