from backend.modules.api.functions import get_db_connection
from backend.utils.anonymize import anonymize_name
from backend.modules.api.models import Patient, PatientCreate, PatientUpdate
from fastapi import APIRouter, HTTPException
from typing import List


router = APIRouter()


@router.get(
    "/patients", response_model=List[Patient], summary="Get all patients"
)
def get_patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT p.id, p.name, p.surname, p.age, p.bmi, p.children, p.charges,
               s.sexe AS sex, f.fumeur AS smoker, r.region
        FROM Patient p
        LEFT JOIN Sexe s ON p.sex = s.id_sex
        LEFT JOIN Fumeur f ON p.smoker = f.id_smoker
        LEFT JOIN Region r ON p.region = r.id_region
        """
    )
    patients = cursor.fetchall()
    conn.close()
    return [Patient(**dict(row)) for row in patients]


@router.get(
    "/patients/{patient_id}",
    response_model=Patient,
    summary="Get a patient by ID",
)
def get_patient(patient_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT p.id, p.name, p.surname, p.age, p.bmi, p.children, p.charges,
               s.sexe AS sex, f.fumeur AS smoker, r.region
        FROM Patient p
        LEFT JOIN Sexe s ON p.sex = s.id_sex
        LEFT JOIN Fumeur f ON p.smoker = f.id_smoker
        LEFT JOIN Region r ON p.region = r.id_region
        WHERE p.id = ?
        """,
        (patient_id,),
    )
    patient = cursor.fetchone()
    conn.close()

    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    return Patient(**dict(patient))


@router.post(
    "/patients", response_model=Patient, summary="Create a new patient"
)
def create_patient(patient: PatientCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Anonymisation du nom et prénom
    anonymized_name = anonymize_name(patient.name)
    anonymized_surname = anonymize_name(patient.surname)

    # Récupérer l'ID correspondant au sexe
    cursor.execute("SELECT id_sex FROM Sexe WHERE sexe = ?", (patient.sex,))
    sex_row = cursor.fetchone()
    if not sex_row:
        raise HTTPException(status_code=400, detail="Invalid value for sex.")
    sex = sex_row["id_sex"]

    # Récupérer l'ID correspondant à la région
    cursor.execute(
        "SELECT id_region FROM Region WHERE region = ?", (patient.region,)
    )
    region_row = cursor.fetchone()
    if not region_row:
        raise HTTPException(
            status_code=400, detail="Invalid value for region."
        )
    region = region_row["id_region"]

    # Récupérer l'ID correspondant à la valeur de fumeur
    cursor.execute(
        "SELECT id_smoker FROM Fumeur WHERE fumeur = ?", (patient.smoker,)
    )
    smoker_row = cursor.fetchone()
    if not smoker_row:
        raise HTTPException(
            status_code=400, detail="Invalid value for smoker."
        )
    smoker = smoker_row["id_smoker"]

    # Insérer le patient dans la table Patient avec les IDs obtenus
    cursor.execute(
        """
        INSERT INTO Patient (name, surname, age, bmi,
        children, smoker, region, charges, sex)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            anonymized_name,
            anonymized_surname,
            patient.age,
            patient.bmi,
            patient.children,
            smoker,
            region,
            patient.charges,
            sex,
        ),
    )

    conn.commit()
    patient_id = cursor.lastrowid
    conn.close()

    return {
        **patient.model_dump(),
        "id": patient_id,
        "name": anonymized_name,
        "surname": anonymized_surname,
    }

@router.put(
    "/patients/{patient_id}",
    response_model=Patient,
    summary="Update a patient",
)
def update_patient(patient_id: int, patient: PatientUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Vérifier si le patient existe
    cursor.execute("SELECT * FROM Patient WHERE id = ?", (patient_id,))
    existing_patient = cursor.fetchone()
    if not existing_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    cursor.execute(
        """
        UPDATE Patient
        SET name = ?, surname = ?, age = ?, bmi = ?, children = ?,
        smoker = ?, region = ?, charges = ?, sex = ?
        WHERE id = ?
        """,
        (
            patient.name,
            patient.surname,
            patient.age,
            patient.bmi,
            patient.children,
            patient.smoker,
            patient.region,
            patient.charges,
            patient.sex,
            patient_id,
        ),
    )

    conn.commit()
    conn.close()

    return {**patient.model_dump(), "id": patient_id}


@router.delete("/patients/{patient_id}", summary="Delete a patient")
def delete_patient(patient_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Vérifier si le patient existe
    cursor.execute("SELECT * FROM Patient WHERE id = ?", (patient_id,))
    existing_patient = cursor.fetchone()
    if not existing_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    cursor.execute("DELETE FROM Patient WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()

    return {"message": "Patient deleted successfully"}
