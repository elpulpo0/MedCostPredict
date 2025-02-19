import sys
from pathlib import Path
import pandas as pd

# Ajouter le répertoire parent à sys.path si nécessaire
sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.modules.preparation.anonymize import anonymize_name

def test_anonymization():
    # Exemple de données de test
    data = {"name": ["Alice", "Bob"], "surname": ["Smith", "Jones"]}
    df = pd.DataFrame(data)

    # Anonymisation
    df["name"] = df["name"].apply(anonymize_name)
    df["surname"] = df["surname"].apply(anonymize_name)

    # Vérification que les noms et prénoms sont anonymisés
    assert len(df["name"][0]) == 64  # SHA256 donne un hachage de 64 caractères
    assert len(df["surname"][0]) == 64
    assert (
        df["name"][0] != "Alice"
    )  # Assurer que le nom original est bien anonymisé
    assert df["surname"][0] != "Smith"
