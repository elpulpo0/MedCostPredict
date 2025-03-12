import os
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
from backend.modules.api.users.security import hash_password

# Charger les variables d'environnement
load_dotenv()

# Définition du chemin du fichier de logs
log_path = Path(__file__).resolve().parents[5] / "logs" / "create_db.log"
logger.add(
    log_path,
    rotation="1 MB",
    level="INFO",
    format="<level>{time:DD-MM-YYYY HH:mm:ss} | {level} | {message}</level>",
)

logger.info("Début de la vérification et génération de la base de données.")

# Définition du chemin de la base de données
DB_PATH = Path("backend/modules/db/users.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Configuration SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Définition du modèle User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")


# Vérifier si la base existe et créer les tables si nécessaire
def init_db():
    """Vérifie si la base de données existe et crée l'admin si besoin."""
    db_exists = DB_PATH.exists()

    if not db_exists:
        logger.info("La base de données n'existe pas. Création en cours...")
        Base.metadata.create_all(bind=engine)
        logger.info("Base de données créée avec succès.")

        # Ajouter l'administrateur depuis le .env
        create_admin_user()

    else:
        logger.info(
            "La base de données existe déjà. Aucun changement nécessaire."
        )


def create_admin_user():
    """Crée un administrateur avec les informations du fichier .env."""
    db: Session = SessionLocal()

    # Vérifier si un admin existe déjà
    existing_admin = db.query(User).filter(User.role == "admin").first()
    if existing_admin:
        logger.info("Un administrateur existe déjà. Aucune action nécessaire.")
        return

    # Récupérer les informations depuis le fichier .env
    admin_name = os.getenv("ADMIN_NAME", "Admin")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@exemple.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "SuperSecure123")

    hashed_password = hash_password(admin_password)

    # Création de l'admin
    admin = User(
        full_name=admin_name,
        email=admin_email,
        hashed_password=hashed_password,
        role="admin",
        is_active=True,
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    logger.info(f"Administrateur {admin.email} créé avec succès.")


if __name__ == "__main__":
    init_db()
