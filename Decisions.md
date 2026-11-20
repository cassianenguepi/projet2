<!-- Fiche de décisions : une ligne par choix important, remplie au fil du projet.
Colonnes : Choix | Options envisagées | Choix retenu et justification | Validé par l'auxiliaire (date) -->

charger_donnees : permet d'ouvrir le fichier csv avec leseparateur ";"
nettoyer() prépare les données pour le modèle 

Variable : la classe parente (le nom de la variable),
VariableNumerique : vérifie qu’une saisie est un nombre dans l’intervalle permis,
VariableCategorielle : vérifie que la saisie fait partie de la liste des valeurs permises,
JeuDeDonnees : contient le tableau et la liste de ces variables.
charger_donnees	un CSV avec ; est bien lu en colonnes, et un fichier introuvable lève FileNotFoundError
nettoyer	le doublon, duration et pdays disparaissent, et deja_contacte vaut 0 ou 1 comme prévu
VariableNumerique	"40" est accepté, les bornes 17 et 98 aussi, et une saisie vide, abc ou hors intervalle lève DonneeInvalideError
VariableCategorielle	une valeur de la liste est acceptée, une valeur inconnue est refusée
JeuDeDonnees	une variable du bon type est créée par colonne, sans la cible y