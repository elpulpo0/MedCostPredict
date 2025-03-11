import pandas as pd
from pathlib import Path
from loguru import logger

from backend.utils.anonymize import anonymize_name

# Chemin pour enregistrer les logs
log_path = Path(__file__).resolve().parents[5] / "logs" / "anonymize.log"
logger.add(
    log_path,
    rotation="1 MB",
    level="INFO",
    format="<level>{time:DD-MM-YYYY HH:mm:ss} | {level} | {message}</level>",
)

logger.info("Début du script d'anonymisation des noms et prénoms.")

csv_path = (
    Path(__file__).resolve().parents[5] / "data" / "insurance_with_names.csv"
)
output_path = (
    Path(__file__).resolve().parents[5] / "data" / "insurance_anonymized.csv"
)


def anonymize_names(input_csv=csv_path, output_csv=output_path):
    """Ajoute les colonnes name et surname à un fichier CSV."""
    try:
        df = pd.read_csv(input_csv)

        # Appliquer l'anonymisation aux colonnes 'name' et 'surname'
        df["name"] = df["name"].apply(anonymize_name)
        df["surname"] = df["surname"].apply(anonymize_name)

        df.to_csv(output_csv, index=False)

        logger.info(f"✅ Fichier anonymisé enregistré à : {output_csv}")

    except Exception as e:
        logger.error(f"❌ Erreur lors de l'ajout des colonnes : {e}")
        raise


if __name__ == "__main__":
    anonymize_names()
