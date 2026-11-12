"""
Tests de src/model.py (pytest).

Couvre : séparation des données, référence, sauvegarde/chargement,
prédiction, et vérification que la métrique NumPy coïncide avec
celle de scikit-learn.
Ne teste pas l'interface.
"""

import os
import numpy as np
import pandas as pd
import pytest

from src.donnees import nettoyer, separer_caracteristiques_cible
from src.model import (    separer_donnees,
    creer_reference,
    entrainer_modele,
    evaluer_modele,
    sauvegarder_modele,
    charger_modele,
    sauvegarder_metadonnees,
    charger_metadonnees,
    predire,
)


@pytest.fixture
def donnees():
    """Prépare un petit jeu de données pour les tests."""
    df = pd.DataFrame({
        "age": [25, 35, 45, 30, 50, 40, 28, 55, 32, 48],
        "job": [
            "admin.", "technician", "services", "admin.",
            "management", "technician", "services", "admin.",
            "management", "technician"
        ],
        "marital": [
            "single", "married", "married", "single", "married",
            "single", "married", "single", "married", "single"
        ],
        "education": [
            "university.degree", "high.school", "basic.9y",
            "university.degree", "professional.course",
            "high.school", "basic.9y", "university.degree",
            "high.school", "professional.course"
        ],
        "default": ["no"] * 10,
        "housing": ["yes", "no"] * 5,
        "loan": ["no", "yes"] * 5,
        "contact": ["cellular"] * 10,
        "month": ["may", "jun"] * 5,
        "day_of_week": ["mon", "tue"] * 5,
        "duration": [100, 200, 150, 180, 120, 220, 160, 190, 140, 210],
        "campaign": [1, 2, 1, 3, 2, 1, 2, 3, 1, 2],
        "pdays": [999, 5, 999, 10, 999, 3, 999, 999, 7, 999],
        "previous": [0, 1, 0, 2, 0, 1, 0, 0, 1, 0],
        "poutcome": ["nonexistent", "success"] * 5,
        "emp.var.rate": [1.1, -1.8] * 5,
        "cons.price.idx": [93.9, 92.8] * 5,
        "cons.conf.idx": [-40.0, -45.0] * 5,
        "euribor3m": [4.8, 1.3] * 5,
        "nr.employed": [5191.0, 5099.0] * 5,
        "y": ["no", "yes"] * 5
    })

    df = nettoyer(df)
    X, y = separer_caracteristiques_cible(df)

    return X, y


def test_separer_donnees(donnees):
    """Vérifie la séparation en ensembles d'entraînement et de test."""
    X, y = donnees

    X_train, X_test, y_train, y_test = separer_donnees(X, y)

    assert len(X_train) == 8
    assert len(X_test) == 2
    assert len(y_train) == 8
    assert len(y_test) == 2


def test_creer_reference(donnees):
    """Vérifie que le modèle de référence apprend la classe majoritaire."""
    X, y = donnees
    X_train, X_test, y_train, y_test = separer_donnees(X, y)

    reference = creer_reference(X_train, y_train)

    assert reference.classes_.tolist() == ["no", "yes"]


def test_entrainer_modele(donnees):
    """Vérifie que le modèle principal peut être entraîné et prédire."""
    X, y = donnees
    X_train, X_test, y_train, y_test = separer_donnees(X, y)

    modele = entrainer_modele(X_train, y_train)
    predictions = modele.predict(X_test)

    assert len(predictions) == len(X_test)
    assert set(predictions).issubset({"yes", "no"})


def test_evaluer_modele(donnees):
    """Vérifie les métriques du modèle et leur calcul avec NumPy."""
    X, y = donnees
    X_train, X_test, y_train, y_test = separer_donnees(X, y)

    modele = entrainer_modele(X_train, y_train)
    reference = creer_reference(X_train, y_train)

    exactitude, exactitude_reference, exactitude_numpy = evaluer_modele(
        modele, reference, X_test, y_test
    )

    assert 0 <= exactitude <= 1
    assert 0 <= exactitude_reference <= 1
    assert exactitude == pytest.approx(exactitude_numpy)


def test_sauvegarder_et_charger_modele(donnees, tmp_path):
    """Vérifie que le modèle sauvegardé peut être rechargé."""
    X, y = donnees
    X_train, X_test, y_train, y_test = separer_donnees(X, y)

    modele = entrainer_modele(X_train, y_train)
    chemin = os.path.join(tmp_path, "modele.pkl")

    sauvegarder_modele(modele, chemin)
    modele_charge = charger_modele(chemin)

    assert modele_charge.predict(X_test).tolist() == modele.predict(X_test).tolist()


def test_charger_modele_fichier_absent(tmp_path):
    """Vérifie l'erreur si le fichier du modèle est absent."""
    chemin = os.path.join(tmp_path, "inexistant.pkl")

    with pytest.raises(FileNotFoundError):
        charger_modele(chemin)


def test_sauvegarder_et_charger_metadonnees(tmp_path):
    """Vérifie la sauvegarde et le chargement des métadonnées."""
    chemin = os.path.join(tmp_path, "metadonnees.json")
    colonnes = ["age", "job", "deja_contacte"]

    sauvegarder_metadonnees(chemin, 0.85, colonnes)
    metadonnees = charger_metadonnees(chemin)

    assert metadonnees["exactitude"] == 0.85
    assert metadonnees["colonnes"] == colonnes


def test_charger_metadonnees_fichier_absent(tmp_path):
    """Vérifie l'erreur si le fichier JSON est absent."""
    chemin = os.path.join(tmp_path, "inexistant.json")

    with pytest.raises(FileNotFoundError):
        charger_metadonnees(chemin)


def test_predire(donnees):
    """Vérifie la prédiction et la probabilité associée."""
    X, y = donnees
    X_train, X_test, y_train, y_test = separer_donnees(X, y)

    modele = entrainer_modele(X_train, y_train)

    prediction, probabilite = predire(modele, X_test.iloc[[0]])

    assert prediction in ["yes", "no"]
    assert 0 <= probabilite <= 1