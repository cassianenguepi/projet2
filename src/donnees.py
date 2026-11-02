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