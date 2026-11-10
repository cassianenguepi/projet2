
"""
Module des données.

Rôle : tout ce qui touche au jeu de données Bank Marketing (UCI).
Contenu :
    - lecture du CSV (séparateur « ; ») avec pandas
    - nettoyage : valeurs « unknown », colonne pdays (999), doublons,
      retrait de la colonne « duration » (fuite de données)
    - classes de variables : Variable (parente), VariableNumerique et
      VariableCategorielle (enfants, chacune valide sa saisie)
    - classe JeuDeDonnees : contient les données et la liste des variables
Ne contient aucun affichage ni code d'interface.
"""

import os

import pandas as pd

from src.exceptions import DonneeInvalideError

CHEMIN_CSV = os.path.join("datas", "bank-additional-full.csv")


def charger_donnees(chemin: str) -> pd.DataFrame:
    """Lit le CSV et renvoie un DataFrame.

    Reçoit : le chemin du fichier CSV.
    Renvoie : un DataFrame pandas.
    Échoue : FileNotFoundError si le fichier n'existe pas.
    """
    if not os.path.exists(chemin):
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    with open(chemin, encoding="utf-8") as fichier:
        return pd.read_csv(fichier, sep=";")


def nettoyer(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie le DataFrame et renvoie une version propre.

    Reçoit : le DataFrame brut.
    Renvoie : un DataFrame sans doublons, sans 'duration' (fuite de données),
    avec 'pdays' remplacée par l'indicateur 'deja_contacte' (0 ou 1).
    Échoue : KeyError si les colonnes 'duration' ou 'pdays' sont absentes.
    """
    df = df.drop_duplicates()
    df = df.drop(columns=["duration"])
    df["deja_contacte"] = (df["pdays"] != 999).astype(int)
    df = df.drop(columns=["pdays"])
    return df


class Variable:
    """Classe parente : une variable d'entrée du modèle."""

    def __init__(self, nom: str):
        self._nom = nom

    @property
    def nom(self) -> str:
        """Nom de la variable (lecture seule)."""
        return self._nom

    def valider(self, saisie: str):
        """Valide une saisie. À redéfinir dans les classes enfants."""
        raise NotImplementedError("Les classes enfants doivent redéfinir valider().")


class VariableNumerique(Variable):
    """Variable numérique avec un intervalle permis."""

    def __init__(self, nom: str, minimum: float, maximum: float):
        super().__init__(nom)
        self._minimum = minimum
        self._maximum = maximum

    def valider(self, saisie: str) -> float:
        """Convertit la saisie en nombre et vérifie qu'elle est dans l'intervalle.

        Échoue : DonneeInvalideError si la saisie est vide, non numérique
        ou hors intervalle.
        """
        if saisie.strip() == "":
            raise DonneeInvalideError(f"{self._nom} : champ vide.")
        try:
            valeur = float(saisie.replace(",", "."))
        except ValueError:
            raise DonneeInvalideError(f"{self._nom} : entrez un nombre.") from None
        if not self._minimum <= valeur <= self._maximum:
            raise DonneeInvalideError(
                f"{self._nom} : la valeur doit être entre "
                f"{self._minimum} et {self._maximum}."
            )
        return valeur


class VariableCategorielle(Variable):
    """Variable catégorielle avec la liste de ses valeurs permises."""

    def __init__(self, nom: str, valeurs: list[str]):
        super().__init__(nom)
        self._valeurs = valeurs

    def valider(self, saisie: str) -> str:
        """Vérifie que la saisie fait partie des valeurs permises.

        Échoue : DonneeInvalideError si la valeur n'est pas dans la liste.
        """
        if saisie not in self._valeurs:
            raise DonneeInvalideError(
                f"{self._nom} : choisissez une valeur de la liste."
            )
        return saisie


class JeuDeDonnees:
    """Contient les données nettoyées et la liste des variables d'entrée."""

    def __init__(self, df: pd.DataFrame):
        self._df = df
        self._variables: list[Variable] = []

    def construire_variables(self) -> list[Variable]:
        """Crée une variable par colonne d'entrée (sauf la cible 'y').

        Renvoie : la liste des variables (numériques ou catégorielles).
        """
        self._variables = []
        for colonne in self._df.columns:
            if colonne == "y":
                continue
            if pd.api.types.is_numeric_dtype(self._df[colonne]):
                var = VariableNumerique(
                    colonne, self._df[colonne].min(), self._df[colonne].max()
                )
            else:
                var = VariableCategorielle(
                    colonne, sorted(self._df[colonne].unique())
                )
            self._variables.append(var)
        return self._variables

    def __str__(self) -> str:
        return (
            f"JeuDeDonnees : {len(self._df)} lignes, "
            f"{len(self._variables)} variables"
        )