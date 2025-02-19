from fastapi import FastAPI, HTTPException
import sqlite3
from typing import List
import os

import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.modules.api.models import Patient

app = FastAPI(
    title="MedCostPredict API",
    description="API for managing patients and medecins in a health system.",
    version="1.0.0",
)


# Fonction pour se connecter à la base de données SQLite
def get_db_connection():
    db_path = os.path.join(
        os.path.dirname(__file__), "modules", "db", "patients.db"
    )
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
    return conn


# Récupérer tous les patients
@app.get(
    "/patients",
    response_model=List[Patient],
    summary="Get all patients",
    description="Fetch all the patients from the database.",
)
def get_patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT p.id, p.name, p.surname, p.age, p.bmi, p.children, p.charges, 
               s.sexe AS sex, f.fumeur AS smoker, r.region 
        FROM Patient p
        LEFT JOIN Sexe s ON p.id_sex = s.id_sex
        LEFT JOIN Fumeur f ON p.smoker = f.id_smoker
        LEFT JOIN Region r ON p.region = r.id_region
    """
    )
    patients = cursor.fetchall()  # Récupérer toutes les lignes
    conn.close()

    # Convertir chaque ligne en un dictionnaire compatible avec le modèle Patient
    return [
        Patient(**{key: row[key] for key in row.keys()}) for row in patients
    ]


# Récupérer un patient par ID
@app.get(
    "/patients/{patient_id}",
    response_model=Patient,
    summary="Get a patient by ID",
    description="Fetch a specific patient using their unique ID.",
)
def get_patient(patient_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT p.id, p.name, p.surname, p.age, p.bmi, p.children, p.charges, 
               s.sexe AS sex, f.fumeur AS smoker, r.region 
        FROM Patient p
        LEFT JOIN Sexe s ON p.id_sex = s.id_sex
        LEFT JOIN Fumeur f ON p.smoker = f.id_smoker
        LEFT JOIN Region r ON p.region = r.id_region
        WHERE p.id = ?
    """,
        (patient_id,),
    )
    patient = cursor.fetchone()  # Récupérer une seule ligne
    conn.close()

    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Convertir la ligne en un dictionnaire compatible avec le modèle Patient
    return Patient(**{key: patient[key] for key in patient.keys()})
