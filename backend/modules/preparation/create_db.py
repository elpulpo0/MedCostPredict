import sqlite3
import pandas as pd
from pathlib import Path
from loguru import logger

# Logger
log_path = Path(__file__).resolve().parents[3] / "logs" / "create_db.log"
logger.add(
    log_path,
    rotation="1 MB",
    level="INFO",
    format="<level>{time:DD-MM-YYYY HH:mm:ss} | {level} | {message}</level>",
)

logger.info("Début de la génération des fichiers complémentaires.")

# Définition des chemins des fichiers CSV
data_dir = Path(__file__).resolve().parents[3] / "data"
patients_file = data_dir / "insurance_anonymized.csv"
medecins_file = data_dir / "medecins.csv"
consultations_file = data_dir / "consultations.csv"
diagnostics_file = data_dir / "diagnostics.csv"

# Connexion à la base de données SQLite
conn = sqlite3.connect("backend/modules/db/patients.db")
cursor = conn.cursor()

# Création des tables (si elles n'existent pas déjà)
cursor.executescript(
    """
    CREATE TABLE IF NOT EXISTS Patient (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        age INTEGER,
        sex TEXT,
        bmi REAL,
        children INTEGER,
        smoker TEXT CHECK(smoker IN ('yes', 'no')),
        region TEXT,
        charges REAL
    );

    CREATE TABLE IF NOT EXISTS Médecin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        specialty TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Consultation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        consultation_date DATE,
        FOREIGN KEY (patient_id) REFERENCES Patient(id),
        FOREIGN KEY (doctor_id) REFERENCES Médecin(id)
    );

    CREATE TABLE IF NOT EXISTS Diagnostique (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        consultation_id INTEGER,
        diagnostic_description TEXT,
        FOREIGN KEY (consultation_id) REFERENCES Consultation(id)
    );
    """
)

# Charger et insérer les patients
df_patients = pd.read_csv(patients_file)
df_patients["id"] = range(1, len(df_patients) + 1)

for _, row in df_patients.iterrows():
    cursor.execute(
        """
        INSERT INTO Patient (id, age, sex, bmi, children, smoker, region, charges, name, surname)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (
            row["id"],
            row["age"],
            row["sex"],
            row["bmi"],
            row["children"],
            row["smoker"],
            row["region"],
            row["charges"],
            row["name"],
            row["surname"],
        ),
    )

# Charger et insérer les médecins
df_medecins = pd.read_csv(medecins_file)
for _, row in df_medecins.iterrows():
    cursor.execute(
        """
        INSERT INTO Médecin (id, name, surname, specialty)
        VALUES (?, ?, ?, ?);
        """,
        (
            row["id"],
            row["name"],
            row["surname"],
            row["specialty"],
        ),
    )

# Charger et insérer les consultations
df_consultations = pd.read_csv(consultations_file)
for _, row in df_consultations.iterrows():
    cursor.execute(
        """
        INSERT INTO Consultation (id, patient_id, doctor_id, consultation_date)
        VALUES (?, ?, ?, ?);
        """,
        (
            row["id"],
            row["patient_id"],
            row["medecin_id"],
            row["date"],
        ),
    )

# Charger et insérer les diagnostics
df_diagnostics = pd.read_csv(diagnostics_file)
for _, row in df_diagnostics.iterrows():
    cursor.execute(
        """
        INSERT INTO Diagnostique (id, consultation_id, diagnostic_description)
        VALUES (?, ?, ?);
        """,
        (
            row["id"],
            row["consultation_id"],
            row["diagnosis"],
        ),
    )

# Commit et fermeture de la connexion
conn.commit()
conn.close()

print(
    "Toutes les données ont été insérées avec succès dans la base de données."
)
