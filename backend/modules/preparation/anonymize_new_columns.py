import pandas as pd
from pathlib import Path
from loguru import logger

from backend.utils.anonymize import anonymize_name

# Chemin pour enregistrer les logs
log_path = Path(__file__).resolve().parents[3] / "logs" / "anonymize.log"
logger.add(
    log_path,
    rotation="1 MB",
    level="INFO",
    format="<level>{time:DD-MM-YYYY HH:mm:ss} | {level} | {message}</level>",
)

logger.info("Début du script d'anonymisation des noms et prénoms.")

# Charger le fichier CSV
csv_path = (
    Path(__file__).resolve().parents[3] / "data" / "insurance_with_names.csv"
)
df = pd.read_csv(csv_path)

# Appliquer l'anonymisation aux colonnes 'name' et 'surname'
df["name"] = df["name"].apply(anonymize_name)
df["surname"] = df["surname"].apply(anonymize_name)

# Sauvegarder le fichier anonymisé
output_path = (
    Path(__file__).resolve().parents[3] / "data" / "insurance_anonymized.csv"
)
df.to_csv(output_path, index=False)

logger.info(f"✅ Fichier anonymisé enregistré à : {output_path}")
