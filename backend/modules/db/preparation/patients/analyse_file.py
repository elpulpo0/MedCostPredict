import pandas as pd
from pathlib import Path
from loguru import logger

log_path = Path(__file__).resolve().parents[5] / "logs" / "data_analysis.log"
logger.add(
    log_path,
    rotation="1 MB",
    level="INFO",
    format="<level>{time:DD-MM-YYYY HH:mm:ss} | {level} | {message}</level>",
)

logger.info("Début de l'analyse du fichier CSV.")

csv_path = (
    Path(__file__).resolve().parents[5] / "data" / "insurance_with_names.csv"
)


def analyze_csv(file_path=csv_path):
    """Analyse le fichier CSV : vérifie les valeurs manquantes, affiche des stats générales et propose un filtrage."""
    try:
        df = pd.read_csv(file_path)

        # Vérification des valeurs manquantes
        missing_values = df.isnull().sum()
        logger.info("✅ Vérification des valeurs manquantes terminée.")
        print("\nValeurs manquantes par colonne :\n", missing_values)

        # Affichage des statistiques générales
        print("\nStatistiques générales :\n", df.describe(include="all"))
        logger.info("✅ Statistiques générales affichées.")

        return df

    except Exception as e:
        logger.error(f"❌ Erreur lors de l'analyse du fichier CSV : {e}")
        raise

if __name__ == "__main__":
    df = analyze_csv()
