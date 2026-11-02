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