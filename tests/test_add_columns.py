import sys
from pathlib import Path
import pytest
import pandas as pd

# Ajouter le répertoire parent à sys.path si nécessaire
sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.modules.preparation.add_columns import add_fake_names

# Chemins de test
TEST_CSV = Path(__file__).resolve().parent / "test_insurance.csv"
TEST_OUTPUT_CSV = (
    Path(__file__).resolve().parent / "test_insurance_with_names.csv"
)


@pytest.fixture
def sample_csv():
    """Crée un fichier CSV temporaire pour le test."""
    df = pd.DataFrame(
        {
            "age": [25, 32, 40],
            "sex": ["male", "female", "male"],
            "bmi": [22.5, 30.1, 27.3],
            "children": [0, 1, 2],
            "smoker": ["no", "yes", "no"],
            "region": ["southwest", "northeast", "northwest"],
            "charges": [3200.5, 4000.0, 5200.75],
        }
    )
    df.to_csv(TEST_CSV, index=False)
    yield TEST_CSV
    TEST_CSV.unlink()  # Supprime le fichier après le test


def test_add_fake_names(sample_csv):
    """Teste l'ajout des colonnes name et surname."""
    df = add_fake_names(sample_csv, TEST_OUTPUT_CSV)

    # Vérifier que les nouvelles colonnes existent
    assert "name" in df.columns
    assert "surname" in df.columns

    # Vérifier que les colonnes ne sont pas vides
    assert df["name"].notnull().all()
    assert df["surname"].notnull().all()

    # Nettoyage
    TEST_OUTPUT_CSV.unlink()
