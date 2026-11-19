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


import csv
import os
import tkinter as tk
from tkinter import ttk

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.donnees import VariableNumerique, VariableCategorielle
from src.exceptions import DonneeInvalideError
from src.model import predire

CHEMIN_HISTORIQUE = os.path.join(
    "models", "historique_predictions.csv"
)

class Application:
    """Gère l'interface graphique de BankPredict."""

    def __init__(self, modele, variables):
        """Initialise la fenêtre et construit les champs de saisie."""

        self.modele = modele
        self.variables = variables
        self.champs = {}

        self.nombre_yes = 0
        self.nombre_no = 0

        self.fenetre = tk.Tk()
        self.fenetre.title("BankPredict")
        self.fenetre.geometry("1050x800")

        self.titre = tk.Label(
            self.fenetre,
            text="BankPredict",
            font=("Arial", 24, "bold")
        )
        self.titre.pack(pady=10)

        self.description = tk.Label(
            self.fenetre,
            text="Prédiction de souscription à un produit bancaire",
            font=("Arial", 12)
        )
        self.description.pack(pady=5)

        self.avertissement = tk.Label(
            self.fenetre,
            text=(
                "Outil pédagogique : les prédictions ne constituent "
                "pas une aide à la décision bancaire."
            ),
            fg="red",
            wraplength=900
        )
        self.avertissement.pack(pady=5)

        # Zone principale contenant les champs et les résultats.
        self.zone_principale = tk.Frame(self.fenetre)
        self.zone_principale.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        # Partie gauche : champs de saisie avec défilement.
        self.zone_champs = tk.Frame(self.zone_principale)
        self.zone_champs.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.canvas = tk.Canvas(self.zone_champs)
        self.barre_defilement = ttk.Scrollbar(
            self.zone_champs,
            orient="vertical",
            command=self.canvas.yview
        )

        self.cadre_champs = tk.Frame(self.canvas)

        self.cadre_champs.bind(
            "<Configure>",
            lambda evenement: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0),
            window=self.cadre_champs,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.barre_defilement.set
        )

        self.canvas.pack(side="left", fill="both", expand=True)
        self.barre_defilement.pack(side="right", fill="y")

        self.construire_champs()

        # Partie droite : résultat et graphique.
        self.zone_resultats = tk.Frame(self.zone_principale)
        self.zone_resultats.pack(
            side="right",
            fill="both",
            expand=True,
            padx=15
        )

        self.resultat = tk.Label(
            self.zone_resultats,
            text="En attente d'une prédiction...",
            font=("Arial", 12),
            wraplength=350
        )
        self.resultat.pack(pady=20)

        self.bouton_prediction = tk.Button(
            self.zone_resultats,
            text="Lancer la prédiction",
            command=self.faire_prediction,
            font=("Arial", 12)
        )
        self.bouton_prediction.pack(pady=10)

        self.creer_graphique()

    def construire_champs(self):
        """Crée un champ de saisie pour chaque variable du modèle."""

        titre = tk.Label(
            self.cadre_champs,
            text="Informations du client",
            font=("Arial", 16, "bold")
        )
        titre.pack(pady=10)

        for variable in self.variables:

            ligne = tk.Frame(self.cadre_champs)
            ligne.pack(fill="x", padx=10, pady=5)

            etiquette = tk.Label(
                ligne,
                text=f"{variable.nom} :",
                width=20,
                anchor="w"
            )
            etiquette.pack(side="left")

            if isinstance(variable, VariableNumerique):

                champ = ttk.Entry(ligne, width=25)
                champ.pack(side="left")

            elif isinstance(variable, VariableCategorielle):

                champ = ttk.Combobox(
                    ligne,
                    values=variable.valeurs,
                    state="readonly",
                    width=23
                )
                champ.pack(side="left")

                if variable.valeurs:
                    champ.current(0)

            self.champs[variable.nom] = champ

    def faire_prediction(self):
        """Valide les champs et effectue une prédiction."""

        nouvelles_donnees = {}
        try:
            for variable in self.variables:
                saisie = self.champs[variable.nom].get()
                valeur = variable.valider(saisie)
                nouvelles_donnees[variable.nom] = valeur

            # Création d'un DataFrame contenant un seul client.
            donnees_client = pd.DataFrame([nouvelles_donnees])

            prediction, probabilite_no, probabilite_yes = predire(
                self.modele,
                donnees_client
            )

            pourcentage_no = probabilite_no * 100
            pourcentage_yes = probabilite_yes * 100

            self.resultat.config(
                text=(
                    f"Résultat : {prediction.upper()}\n"
                    f"Probabilité NO : {pourcentage_no:.2f} %\n"
                    f"Probabilité YES : {pourcentage_yes:.2f} %"
            )
        )

            self.enregistrer_prediction(
                nouvelles_donnees,
                prediction,
                probabilite_no, 
                probabilite_yes
            )

            self.mettre_a_jour_graphique(prediction)

        except DonneeInvalideError as erreur:

            self.resultat.config(
                text=f"Erreur de saisie : {erreur}"
            )

        except Exception as erreur:

            self.resultat.config(
                text=f"Une erreur est survenue : {erreur}"
            )

    def enregistrer_prediction(
        self,
        donnees_client,
        prediction,
        probabilite_no, 
        probabilite_yes
    ):
        """Ajoute une prédiction et ses probabilités à l'historique CSV."""

        dossier = os.path.dirname(CHEMIN_HISTORIQUE)

        if dossier:
            os.makedirs(dossier, exist_ok=True)

        fichier_existe = os.path.exists(CHEMIN_HISTORIQUE)

        with open(
            CHEMIN_HISTORIQUE,
            "a",
            newline="",
            encoding="utf-8"
        ) as fichier:

            colonnes = (
                list(donnees_client.keys())
                + ["prediction", "probabilite_no", "probabilite_yes"]
            )

            ecrivain = csv.DictWriter(
                fichier,
                fieldnames=colonnes
            )

            if not fichier_existe:
                ecrivain.writeheader()

            ligne = donnees_client.copy()
            ligne["prediction"] = prediction
            ligne["probabilite_no"] = probabilite_no
            ligne["probabilite_yes"] = probabilite_yes

            ecrivain.writerow(ligne)

    def creer_graphique(self):
        """Crée un graphique des prédictions de la session."""

        self.figure = Figure(figsize=(4, 3), dpi=100)
        self.axes = self.figure.add_subplot(111)

        self.canvas_graphique = FigureCanvasTkAgg(
            self.figure,
            master=self.zone_resultats
        )

        self.canvas_graphique.get_tk_widget().pack(
            fill="both",
            expand=True,
            pady=20
        )

        self.mettre_a_jour_graphique()

    def mettre_a_jour_graphique(self, prediction=None):
        """Actualise le graphique des prédictions."""

        if prediction == "yes":
            self.nombre_yes += 1

        elif prediction == "no":
            self.nombre_no += 1

        self.axes.clear()

        categories = ["yes", "no"]
        nombres = [self.nombre_yes, self.nombre_no]

        self.axes.bar(categories, nombres)
        self.axes.set_title("Prédictions de la session")
        self.axes.set_ylabel("Nombre de prédictions")

        self.canvas_graphique.draw()
    
    def lancer(self):
        """Lance la boucle principale de l'interface."""
        self.fenetre.mainloop()
        