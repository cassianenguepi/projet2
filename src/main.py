"""
Point d'entrée du projet.

Rôle : démarrer l'application.
Contenu : crée l'Application et la lance. Aucune logique ici.
Lancement : python -m src.main (depuis la racine du projet)
"""

import os

from src.donnees import (
    CHEMIN_CSV,
    JeuDeDonnees,
    charger_donnees,
    nettoyer
)

from src.model import (
    preparer_modele,
    charger_modele
)

from src.interface import Application


CHEMIN_MODELE = os.path.join("models", "modele.pkl")
CHEMIN_METADONNEES = os.path.join("models", "metadonnees.json")


def main() -> None:
    """Prépare les données, charge le modèle et lance l'interface."""

    try:
        # Entraîne le modèle si les fichiers nécessaires sont absents.
        if (
            not os.path.exists(CHEMIN_MODELE)
            or not os.path.exists(CHEMIN_METADONNEES)
        ):
            print("Aucun modèle complet trouvé.")
            print("Entraînement du modèle en cours...")

            resultats = preparer_modele()

            print("Entraînement terminé.")
            print(f"Exactitude du modèle : {resultats[0]:.4f}")
            print(f"Exactitude de référence : {resultats[1]:.4f}")
            print(f"Exactitude calculée avec NumPy : {resultats[2]:.4f}")

        # Charge le modèle entraîné.
        modele = charger_modele(CHEMIN_MODELE)

        # Charge les données et construit les variables de l'interface.
        df = charger_donnees(CHEMIN_CSV)
        df = nettoyer(df)

        jeu = JeuDeDonnees(df)
        variables = jeu.construire_variables()

        print(jeu)
        print("Ouverture de BankPredict...")

        # Lance l'interface.
        application = Application(modele, variables)
        application.lancer()

    except (FileNotFoundError, ImportError) as erreur:
        print(f"Erreur : {erreur}")
        print(
            "Vérifiez la présence du CSV dans datas/ "
            "et les dépendances du projet."
        )

if __name__ == "__main__":
    main()

# Pour lancer l'interface: python3 -m src.main

