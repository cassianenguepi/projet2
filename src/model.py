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