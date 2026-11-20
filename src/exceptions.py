"""
Module des exceptions personnalisées.

Rôle : regrouper les erreurs propres au projet.
Contenu 
    - DonneeInvalideError(Exception) : levée quand une saisie est vide,
      non numérique, hors intervalle ou hors des valeurs permises
"""
class DonneeInvalideError(Exception):
    pass
# from src.exceptions import DonneeInvalideError("Test")
# try:
#     raise DonneeInvalideError("Test")
# except DonneeInvalideError as e:
#     print(e) # apparament il ne fait pas garder ceci