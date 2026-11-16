"""
Point d'entrée du projet.
from src.donnees import CHEMIN_CSV,JEUDEDONNEES,charger_donnees,nettoyer
Rôle : démarrer l'application.
Contenu : crée l'Application et la lance. Aucune logique ici.
Lancement : python -m src.main (depuis la racine du projet)
"""
from src.donnees import CHEMIN_CSV,JeuDeDonnees,charger_donnees,nettoyer
from src.interface import Application
from src.model import Modele 


def main() -> None:
    "assemble les composants et lance l'interface"
    try:
        jeu =  JeuDeDonnees(nettoyer(charger_donnees(CHEMIN_CSV)))
        modele = Modele.charger()
    except FileNotFoundError as erreur :
        print(f"Erreur:{erreur}")
        print("Verifiez que le csv est dans datas/et que le modele a été entrainé.")
        return 
    application = Application(modele,jeu.construire_variables())
    application.lancer()


if __name__ == "__main__":
    main()