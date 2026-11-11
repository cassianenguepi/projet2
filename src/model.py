"""
Module du modèle.

Rôle : entraîner, évaluer, sauvegarder et utiliser le modèle de classification.
Contenu :
    - séparation entraînement/test (train_test_split, graine fixée)
    - modèle de référence (classe majoritaire)
    - entraînement et évaluation (métrique choisie, comparée à la référence)
    - métrique recalculée avec NumPy (calcul vectorisé)
    - sauvegarde et chargement : modèle (joblib) et métadonnées (JSON)
    - prédiction avec probabilité
Ne contient aucun affichage ni code d'interface.
"""

import numpy as np
import json
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

def separer_donnees(X, y):
    """
        Sépare les données en ensembles d'entrainement et de test
        X : caractéristiques du client
        y : variable cible (yes or no)
    """

    # Fonction qui retourne 4 résultats : 80 % données de X et y dans train, et 20% dans test
    X_train, X_test, y_train, y_test = train_test_split(
        X, 
        y, 
        test_size=0.2, # quantité de données réservées (20% des observations) pour le test
        random_state=42, # "permet de reproduire la même séparation des données chaque fois qu'on execute la fonction
        stratify=y # permet de conserver les mêmes proportions de "yes" et "no" dans l'entrainement et le test
    )
    return X_train, X_test, y_train, y_test

def creer_reference(X_train, y_train):
    """
        Crée et entraine un modèle de référence (reference); prédit en fonction de la catégorie (yes, no) la plus fréquente
        X_train : caractéristiques d'entrainement
        y_train : réponses attendues pour l'entrainement
    """
    reference = DummyClassifier(strategy="most_frequent") # strategy : indique que DummyClassifier va prédire la catégorie la plus fréquente
    reference.fit(X_train, y_train) # .fit() : apprend quelle catégorie est majoritaire
    return reference

def entrainer_modele(X_train, y_train):
    """
        Crée et entraine un modèle de classification (modele); prédit en fonction des caratéristiques des observations
        X_train : caractéristiques d'entrainement
        y_train : réponses attendues pour l'entrainement
    """
    # Création d'une Pipeline (regrouper les transformations et le modèle)
    # Utilisation de ColumnTransformer et de OneHotEncoder pour transformer les catégories textuelles en colonnes numériques
    # DecisionTreeClassifier cherche les divisions de données qui sont plus souvent associés à un yes ou no pour faire une prédiction
    colonnes_categorielles = [
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "poutcome"
]
    # preprocesseur transforme les variables catégorielles
    # remainder="passthrough" sert à conserver les colonnes numériques
    preprocesseur = ColumnTransformer(transformers=[("categoriel", OneHotEncoder(handle_unknown="ignore"), colonnes_categorielles)], remainder="passthrough")
    modele = Pipeline([
    ("preprocesseur", preprocesseur),
    ("classificateur", DecisionTreeClassifier(random_state=42))
])
    modele.fit(X_train, y_train) # entrainement avec les données
    return modele

def evaluer_modele(modele, reference, X_test, y_test):
    """ 
        Évaluer les performances du modèle principal et de reference et vérification avec Numpy
    """
    # Évaluation du modele principal
    y_pred = modele.predict(X_test) # y prédit à partir de données de clients jamais rencontrés lors de l'entrainement
    exactitude = accuracy_score(y_test, y_pred) # comparaison et calcul taux d'exactitude (accuracy)
   # Évaluation du modèle de référence
    y_pred_reference = reference.predict(X_test)
    exactitude_reference = accuracy_score(y_test, y_pred_reference)
    # Vérification avec Numpy
    exactitude_numpy = np.mean(np.array(y_test) == np.array(y_pred)) # comparaison donne des booléens (True = 1, False = 0) et fait leur moyenne

    return exactitude, exactitude_reference, exactitude_numpy

def sauvegarder_modele(modele, chemin):
    """ 
        Sauvegarde le modele entrainé 
        modele : modele entrainé
        chemin : emplacement du fichier de sauvegarde
    """
    dossier = os.path.dirname(chemin)
    if dossier and not os.path.exists(dossier):
        raise FileNotFoundError("Le dossier de destination n'existe pas.")
    joblib.dump(modele, chemin) # sauvegarde le modele entrainé (apprentissage)

def charger_modele(chemin):
    """ Récupère le modèle sauvegarder"""
    if not os.path.exists(chemin):
        raise FileNotFoundError("Le fichier du modèle est introuvable.")
    modele = joblib.load(chemin)
    return modele

def sauvegarder_metadonnees(chemin, exactitude, colonnes):
    """ Sauvegarde les métadonnées du modele dans un fichier JSON """
    dossier = os.path.dirname(chemin)
    if dossier and not os.path.exists(dossier):
        raise FileNotFoundError("Le dossier de destination n'existe pas.")

    metadonnees = {
        "nom_modele": "Arbre de décision",
        "exactitude" : exactitude, 
        "colonnes" : colonnes
    }
    with open(chemin, "w", encoding="utf-8") as fichier:
        json.dump(metadonnees, fichier, indent=4)

def charger_metadonnees(chemin):
    """ Charge les métadonnees depuis un fichier JSON"""
    if not os.path.exists(chemin):
        raise FileNotFoundError("Le fichier des métadonnées est introuvable.")
    with open(chemin, "r", encoding="utf-8") as fichier:
        metadonnees = json.load(fichier) # dictionnaire 

    return metadonnees

def predire(modele, nouvelles_donnees):
    """
    Prédit la souscription d'un client et retourne
    la probabilité associée à la prédiction.

    Paramètres :
        modele : modèle de classification entraîné.
        nouvelles_donnees : caractéristiques du nouveau client.
    """
    prediction = modele.predict(nouvelles_donnees)[0] # modele entrainé utilise les caractéristique du nouveau client pour faire une prédiction, [0] retire liste
    probabilites = modele.predict_proba(nouvelles_donnees)[0]
    classes = modele.classes_ # associé au yes, no --> liste triée ne ordre alphabétique ["no", "yes"]
    indice = list(classes).index(prediction) # récupérer la prédictiom
    probabilite = probabilites[indice]
    return prediction, probabilite # retourn yes or no et probabilite associée à la catégorie prédite