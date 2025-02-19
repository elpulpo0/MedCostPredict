from pydantic import BaseModel


# Modèle de données pour un patient (utilisé pour la validation)
class Patient(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    sex: str  # sex est maintenant une chaîne ("Male" ou "Female")
    bmi: float
    children: int
    smoker: str  # smoker est maintenant une chaîne ("oui" ou "non")
    region: str  # region est une chaîne (nom de la région)
    charges: float

    class Config:
        orm_mode = True  # Permet à Pydantic de travailler avec les ORM et les résultats SQL
