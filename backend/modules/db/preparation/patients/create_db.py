import sqlite3
import pandas as pd
from pathlib import Path
from loguru import logger

# Logger
log_path = Path(__file__).resolve().parents[5] / "logs" / "create_db.log"
logger.add(
    log_path,
    rotation="1 MB",
    level="INFO",
    format="<level>{time:DD-MM-YYYY HH:mm:ss} | {level} | {message}</level>",
)

logger.info("Début de la génération de la base de données 'Patients'.")

# Définir le chemin du fichier CSV
data_dir = Path(__file__).resolve().parents[5] / "data"
patients_file = data_dir / "insurance_anonymized.csv"

# Connexion à la base de données SQLite
conn = sqlite3.connect("backend/modules/db/patients.db")
cursor = conn.cursor()

# Création des tables
cursor.executescript(
    """
    CREATE TABLE IF NOT EXISTS Sexe (
        id_sex INTEGER PRIMARY KEY AUTOINCREMENT,
        sexe TEXT NOT NULL -- Homme ou Femme
    );

    CREATE TABLE IF NOT EXISTS Fumeur (
        id_smoker INTEGER PRIMARY KEY AUTOINCREMENT,
        fumeur TEXT CHECK(fumeur IN ('yes', 'no')) -- Oui ou Non
    );

    CREATE TABLE IF NOT EXISTS Region (
        id_region INTEGER PRIMARY KEY AUTOINCREMENT,
        region TEXT NOT NULL -- Nom de la région
    );

    CREATE TABLE IF NOT EXISTS Patient (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        age INTEGER,
        sex INTEGER,
        bmi REAL,
        children INTEGER,
        smoker INTEGER,
        region INTEGER,
        charges REAL,
        FOREIGN KEY (sex) REFERENCES Sexe(id_sex),
        FOREIGN KEY (smoker) REFERENCES Fumeur(id_smoker),
        FOREIGN KEY (region) REFERENCES Region(id_region)
    );
    """
)

# Charger le fichier CSV des patients
df_patients = pd.read_csv(patients_file)

# Insérer les valeurs dans les tables
sex_values = df_patients["sex"].unique()
smoker_values = df_patients["smoker"].unique()
region_values = df_patients["region"].unique()

# Insérer les valeurs dans la table Sexe
for sex in sex_values:
    cursor.execute("INSERT OR IGNORE INTO Sexe (sexe) VALUES (?);", (sex,))

# Insérer les valeurs dans la table Fumeur
for smoker in smoker_values:
    cursor.execute(
        "INSERT OR IGNORE INTO Fumeur (fumeur) VALUES (?);", (smoker,)
    )

# Insérer les valeurs dans la table Region
for region in region_values:
    cursor.execute(
        "INSERT OR IGNORE INTO Region (region) VALUES (?);", (region,)
    )

# Commit pour valider les insertions dans Sexe, Fumeur et Region
conn.commit()

# Insérer les données des patients dans la table Patient
for _, row in df_patients.iterrows():
    # Récupérer les ID correspondant aux valeurs de sexe, fumeur et région
    cursor.execute("SELECT id_sex FROM Sexe WHERE sexe = ?", (row["sex"],))
    id_sex = cursor.fetchone()
    id_sex = id_sex[0] if id_sex else None  # Si aucun résultat, définir à None

    cursor.execute(
        "SELECT id_smoker FROM Fumeur WHERE fumeur = ?", (row["smoker"],)
    )
    id_smoker = cursor.fetchone()
    id_smoker = (
        id_smoker[0] if id_smoker else None
    )  # Si aucun résultat, définir à None

    cursor.execute(
        "SELECT id_region FROM Region WHERE region = ?", (row["region"],)
    )
    id_region = cursor.fetchone()
    id_region = (
        id_region[0] if id_region else None
    )  # Si aucun résultat, définir à None

    # Insérer les données du patient
    cursor.execute(
        """
        INSERT INTO Patient (name, surname, age, sex,
        bmi, children, smoker, region, charges)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (
            row["name"],
            row["surname"],
            row["age"],
            id_sex,
            row["bmi"],
            row["children"],
            id_smoker,
            id_region,
            row["charges"],
        ),
    )

# Commit et fermeture de la connexion
conn.commit()
conn.close()

logger.info(
    "Les données ont été insérées avec succès dans la base de données."
)
