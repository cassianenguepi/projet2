"""
Module de l'interface graphique.

Rôle : ce que voit et utilise l'utilisateur.
Contenu :
    - classe Application : contient le modèle et la liste des variables
    - champs de saisie construits à partir du fichier JSON de métadonnées
    - validation des saisies : message clair, jamais de plantage
    - bouton « Prédire » : résultat compréhensible et probabilité
    - graphique Matplotlib intégré à la fenêtre
    - historique des prédictions (fichier CSV)
    - avertissement : outil pédagogique, non une aide à la décision
L'interface appelle la logique de donnees.py et model.py, elle ne la contient pas.
"""


import tkinter as tk

class Application:
    """ Gère l'inerface graphique de BankPredict"""
    def __init__(self):
        """ 
        Initialise la fenêtre principale 
        Crée titre, description, résultat, bouton de prédiction et champs de saise de l'âge
        """
        # Fenêtre principale
        self.fenetre = tk.Tk()
        self.fenetre.title("BankPredict")
        self.fenetre.geometry("900x650")
        # Titre
        self.titre = tk.Label(self.fenetre, text="BankPredict", font=("Arial", 24))
        self.titre.pack(pady=20) # positionne les éléments dans la fenêtre
        # Description
        self.description = tk.Label(self.fenetre, text="Prédiction de souscription à un produit bancaire")
        self.description.pack(pady=10)
        # Résultat
        self.resultat = tk.Label(self.fenetre, text="En attente d'une prédiction...")
        self.resultat.pack(pady=20)
        # Champ de saisie de l'âge
        self.label_age = tk.Label(self.fenetre, text="Âge du client :")
        self.label_age.pack(pady=5)
        self.champ_age = tk.Entry(self.fenetre)
        self.champ_age.pack(pady=5)
        # Bouton
        self.bouton_prediction = tk.Button(self.fenetre, text="Lancer la prédiction", command=self.faire_prediction)
        self.bouton_prediction.pack(pady=20)

    def faire_prediction(self):
        """
        Récupère et valide l'âge saisi par l'utilisateur
        """
        age = self.champ_age.get()
        if age == "":
            self.resultat.config(text="Veuillez entrer un âge.")
            return
        try:
            age = int(age)
            if age < 0:
                self.resultat.config(text="Veuillez entrer un âge valide.")
                return
            self.resultat.config(text=f"Âge saisi : {age}")
        except ValueError:
            self.resultat.config(text="Veuillez entrer un nombre entier.")

    def lancer(self):
        """Lancer la boucle principale de l'interface graphique """
        self.fenetre.mainloop()

        