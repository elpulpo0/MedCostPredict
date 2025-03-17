import pandas as pd
import sys
import os
from pathlib import Path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
)

from backend.utils.security import anonymize
from backend.utils.logger import setup_logger

logger = setup_logger(log_name="anonymize_new_columns")

def anonymize_names(input_csv, output_csv):
    """Charge un fichier CSV, anonymise les colonnes 'name' et 'surname', et retourne le DataFrame modifié."""
    logger.info(f"Chargement du fichier CSV : {input_csv}")

    try:
        # Charger le fichier CSV
        df = pd.read_csv(input_csv)
        logger.info(
            f"Fichier CSV chargé avec succès. Nombre de lignes : {len(df)}"
        )

        # Appliquer l'anonymisation aux colonnes 'name' et 'surname'
        logger.info("Anonymisation des noms et prénoms en cours...")
        df["name"] = df["name"].apply(anonymize)
        df["surname"] = df["surname"].apply(anonymize)
        logger.info("Anonymisation des colonnes 'name' et 'surname' terminée.")

        # Sauvegarder le fichier anonymisé
        df.to_csv(output_csv, index=False)
        logger.info(f"Fichier anonymisé enregistré à : {output_csv}")

        # Retourner le DataFrame modifié
        return df

    except FileNotFoundError:
        logger.error(f"Le fichier {input_csv} n'a pas été trouvé.")
        raise

    except pd.errors.EmptyDataError:
        logger.error(f"Le fichier {input_csv} est vide.")
        raise

    except Exception as e:
        logger.error(
            f"Erreur lors de l'anonymisation des noms et prénoms : {e}"
        )
        raise


logger.info("Début du script d'anonymisation des noms et prénoms.")

csv_path = (
    Path(__file__).resolve().parents[5] / "data" / "insurance_with_names.csv"
)
output_path = (
    Path(__file__).resolve().parents[5] / "data" / "insurance_anonymized.csv"
)


if __name__ == "__main__":
    anonymize_names(csv_path, output_path)
