
"""
Tests de src/donnees.py (pytest).

Couvre : cas usuels, cas limites et cas d'erreur
(pytest.raises pour DonneeInvalideError, pytest.approx pour les flottants).
Ne teste pas l'interface.
"""

import pandas as pd
import pytest

from src.donnees import (
    JeuDeDonnees,
    VariableCategorielle,
    VariableNumerique,
    charger_donnees,
    nettoyer,
)
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


# ---------- Lecture du fichier ----------

def test_charger_donnees_cas_usuel(tmp_path):
    """Un CSV avec séparateur ';' est lu en colonnes distinctes."""
    fichier = tmp_path / "test.csv"
    fichier.write_text("age;job;y\n30;admin.;no\n45;services;yes\n", encoding="utf-8")
    df = charger_donnees(str(fichier))
    assert df.shape == (2, 3)
    assert list(df.columns) == ["age", "job", "y"]


def test_charger_donnees_fichier_introuvable():
    """Un chemin inexistant lève FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        charger_donnees("fichier_qui_nexiste_pas.csv")


# ---------- Nettoyage ----------

def test_nettoyer(petit_df):
    """Le nettoyage retire le doublon, 'duration' et 'pdays', et ajoute 'deja_contacte'."""
    propre = nettoyer(petit_df)
    assert len(propre) == 3                      # 1 doublon retiré
    assert "duration" not in propre.columns
    assert "pdays" not in propre.columns
    assert list(propre["deja_contacte"]) == [0, 1, 0]   # 999 -> 0, sinon 1


# ---------- VariableNumerique ----------

def test_variable_numerique_cas_usuel():
    """Une saisie valide est convertie en nombre (virgule acceptée)."""
    var = VariableNumerique("age", 17, 98)
    assert var.valider("40") == pytest.approx(40.0)
    assert var.valider("40,5") == pytest.approx(40.5)


def test_variable_numerique_cas_limite():
    """Les bornes de l'intervalle sont acceptées."""
    var = VariableNumerique("age", 17, 98)
    assert var.valider("17") == pytest.approx(17.0)
    assert var.valider("98") == pytest.approx(98.0)


@pytest.mark.parametrize("saisie", ["", "   ", "abc", "16", "99"])
def test_variable_numerique_saisie_invalide(saisie):
    """Vide, non numérique ou hors intervalle : DonneeInvalideError."""
    var = VariableNumerique("age", 17, 98)
    with pytest.raises(DonneeInvalideError):
        var.valider(saisie)


# ---------- VariableCategorielle ----------

def test_variable_categorielle_cas_usuel():
    """Une valeur de la liste est acceptée telle quelle."""
    var = VariableCategorielle("job", ["admin.", "retired"])
    assert var.valider("retired") == "retired"


def test_variable_categorielle_valeur_inconnue():
    """Une valeur absente de la liste lève DonneeInvalideError."""
    var = VariableCategorielle("job", ["admin.", "retired"])
    with pytest.raises(DonneeInvalideError):
        var.valider("astronaute")


# ---------- JeuDeDonnees ----------

def test_jeu_de_donnees_construit_les_variables(petit_df):
    """Une variable par colonne d'entrée, du bon type, sans la cible 'y'."""
    jeu = JeuDeDonnees(nettoyer(petit_df))
    variables = jeu.construire_variables()
    noms = [v.nom for v in variables]
    assert "y" not in noms
    assert "age" in noms and "job" in noms
    par_nom = {v.nom: v for v in variables}
    assert isinstance(par_nom["age"], VariableNumerique)
    assert isinstance(par_nom["job"], VariableCategorielle)