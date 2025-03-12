import sqlite3
from pathlib import Path

# Définition du chemin absolu
db_path = Path(__file__).resolve().parents[3] / "modules/db/patients.db"


def get_db_connection():
    """Retourne une connexion SQLite à la base de données."""
    if not db_path.exists():
        raise Exception(f"❌ Erreur : Le fichier {db_path} n'existe pas.")

    conn = sqlite3.connect(db_path)
    return conn
