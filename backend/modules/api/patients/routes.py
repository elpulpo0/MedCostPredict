from backend.modules.api.patients.functions import get_db_connection
from backend.utils.security import anonymize
from backend.modules.api.patients.models import (
    Patient,
    PatientCreate,
    PatientUpdate,
)
from backend.modules.api.users.routes import users_router
from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()

router.include_router(users_router)


@router.get(
    "/patients",
    response_model=List[Patient],
    summary="Get all patients",
    tags=["Données des patients"],
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
    columns = [desc[0] for desc in cursor.description]
    patients_list = [dict(zip(columns, row)) for row in patients]

    return patients_list


@router.get(
    "/patients/{patient_id}",
    response_model=Patient,
    summary="Get a patient by ID",
    tags=["Données des patients"],
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

    columns = [desc[0] for desc in cursor.description]
    patient_dict = dict(zip(columns, patient))

    return patient_dict


@router.post(
    "/patients",
    response_model=Patient,
    summary="Create a new patient",
    tags=["Données des patients"],
)
def create_patient(patient: PatientCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Anonymisation du nom et prénom
    anonymized_name = anonymize(patient.name)
    anonymized_surname = anonymize(patient.surname)

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
    tags=["Données des patients"],
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


@router.delete(
    "/patients/{patient_id}",
    summary="Delete a patient",
    tags=["Données des patients"],
)
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
