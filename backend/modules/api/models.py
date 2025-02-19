from pydantic import BaseModel


# Modèle principal pour l'affichage des patients
class Patient(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    sex: str
    bmi: float
    children: int
    smoker: str
    region: str
    charges: float


# Modèle pour la création d'un patient (sans ID)
class PatientCreate(BaseModel):
    name: str
    surname: str
    age: int
    sex: int
    bmi: float
    children: int
    smoker: str
    region: str
    charges: float


# Modèle pour la mise à jour d'un patient
class PatientUpdate(BaseModel):
    name: str
    surname: str
    age: int
    sex: int
    bmi: float
    children: int
    smoker: str
    region: str
    charges: float
