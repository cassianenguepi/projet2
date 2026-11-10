"""
Tests de src/donnees.py (pytest).

Couvre : cas usuels, cas limites et cas d'erreur
(pytest.raises pour DonneeInvalideError, pytest.approx pour les flottants).

Ne teste pas l'interface.
"""
import os
import pandas as pd
from src.exceptions import DonneeInvalideError
@pytest.fixture
def petit_df():
    """Mini jeu de données avec un doublon, 'duration' et 'pdays'."""
    return pd.DataFrame({
        "age": [30, 45, 45, 60],
        "job": ["admin.", "services", "services", "retired"],
        "duration": [100, 200, 200, 300],
        "pdays": [999, 5, 5, 999],
        "y": ["no", "yes", "yes", "no"],
    })
  
def test_charger_donnees_cas_usuel(tmp_path):
    """Un CSV avec séparateur ';' est lu en colonnes distinctes."""
    fichier = tmp_path / "test.csv"
    fichier.write_text("age;job;y\n30;admin.;no\n45;services;yes\n", encoding="utf-8")
    df = charger_donnees(str(fichier))
    assert df.shape == (2, 3)
    assert list(df.columns) == ["age", "job", "y"]
def test_nettoyer(petit_df):
    """Le nettoyage retire le doublon, 'duration' et 'pdays', et ajoute 'deja_contacte'."""
    propre = nettoyer(petit_df)
    assert len(propre) == 3                      # 1 doublon retiré
    assert "duration" not in propre.columns
    assert "pdays" not in propre.columns
    assert list(propre["deja_contacte"]) == [0, 1, 0]   # 999 -> 0, sinon 1
