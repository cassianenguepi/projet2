"""
Point d'entrée du projet.

Rôle : démarrer l'application.
Contenu : crée l'Application et la lance. Aucune logique ici.
Lancement : python -m src.main (depuis la racine du projet)
"""
from src.interface import Application

if __name__ == "__main__":
    application = Application()
    application.lancer()