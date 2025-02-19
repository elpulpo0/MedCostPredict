import pandas as pd
from faker import Faker
from pathlib import Path
from loguru import logger

log_path = Path(__file__).resolve().parents[4] / "logs" / "add_columns.log"
logger.add(
    log_path,
    rotation="1 MB",
    level="INFO",
    format="<level>{time:DD-MM-YYYY HH:mm:ss} | {level} | {message}</level>",
)

logger.info("Début du script d'ajout de colonnes.")

fake = Faker("en_US")

csv_path = Path(__file__).resolve().parents[3] / "data" / "insurance.csv"
output_path = Path(__file__).resolve().parents[3] / "data" / "insurance_with_names.csv"


def add_fake_names(input_csv=csv_path, output_csv=output_path):
    """Ajoute les colonnes name et surname à un fichier CSV."""
    try:
        df = pd.read_csv(input_csv)

        # Ajout des colonnes Faker
        df["name"] = [fake.first_name() for _ in range(len(df))]
        df["surname"] = [fake.last_name() for _ in range(len(df))]

        df.to_csv(output_csv, index=False)

        logger.info(f"✅ Fichier mis à jour enregistré à : {output_csv}")
        return df  # Retourner le DataFrame pour les tests

    except Exception as e:
        logger.error(f"❌ Erreur lors de l'ajout des colonnes : {e}")
        raise


if __name__ == "__main__":
    add_fake_names()
