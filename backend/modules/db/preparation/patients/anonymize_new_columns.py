from pathlib import Path
from loguru import logger
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../..")))

from backend.utils.anonymize import anonymize_names

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


if __name__ == "__main__":
    anonymize_names(csv_path, output_path)
