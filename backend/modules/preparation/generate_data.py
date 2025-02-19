import pandas as pd
from faker import Faker
import random
from pathlib import Path
from loguru import logger

# Initialisation
fake = Faker("en_US")

# Chemins des fichiers
data_dir = Path(__file__).resolve().parents[3] / "data"
insurance_file = data_dir / "insurance.csv"
medecins_file = data_dir / "medecins.csv"
consultations_file = data_dir / "consultations.csv"
diagnostics_file = data_dir / "diagnostics.csv"

# Logger
log_path = Path(__file__).resolve().parents[3] / "logs" / "generate_data.log"
logger.add(
    log_path,
    rotation="1 MB",
    level="INFO",
    format="<level>{time:DD-MM-YYYY HH:mm:ss} | {level} | {message}</level>",
)

logger.info("Début de la génération des fichiers complémentaires.")

# Charger les patients depuis insurance.csv
df_patients = pd.read_csv(insurance_file)
df_patients["id"] = range(1, len(df_patients) + 1)

# Générer les médecins
num_medecins = 10
medecins = [
    {
        "id": i + 1,
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "specialty": random.choice(
            [
                "Cardiology",
                "Neurology",
                "General Medicine",
                "Dermatology",
                "Pediatrics",
            ]
        ),
    }
    for i in range(num_medecins)
]

df_medecins = pd.DataFrame(medecins)
df_medecins.to_csv(medecins_file, index=False)
logger.info(f"✅ Fichier médecins enregistré : {medecins_file}")

# Générer les consultations
consultations = [
    {
        "id": i + 1,
        "patient_id": random.choice(df_patients["id"].tolist()),
        "medecin_id": random.randint(1, num_medecins),
        "date": fake.date_between(start_date="-2y", end_date="today").strftime(
            "%Y-%m-%d"
        ),
    }
    for i in range(
        len(df_patients) // 2
    )  # Environ 50% des patients ont une consultation
]

df_consultations = pd.DataFrame(consultations)
df_consultations.to_csv(consultations_file, index=False)
logger.info(f"✅ Fichier consultations enregistré : {consultations_file}")

# Générer les diagnostics pour les consultations
diagnostics = [
    {
        "id": i + 1,
        "consultation_id": row["id"],
        "diagnosis": random.choice(
            [
                "Hypertension",
                "Diabete",
                "Flu",
                "Covid-19",
                "Allergy",
                "Fracture",
            ]
        ),
    }
    for i, row in df_consultations.iterrows()
]

df_diagnostics = pd.DataFrame(diagnostics)
df_diagnostics.to_csv(diagnostics_file, index=False)
logger.info(f"✅ Fichier diagnostics enregistré : {diagnostics_file}")

logger.info("Génération des fichiers terminée avec succès.")
