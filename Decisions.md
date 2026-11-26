<!-- Fiche de décisions : une ligne par choix important, remplie au fil du projet.
Colonnes : Choix | Options envisagées | Choix retenu et justification | Validé par l'auxiliaire (date) -->

<<<<<<< HEAD
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
=======
1. Entrainement et utilisation du modele: Model.py
Ce fichier contient les fonctions qui créent, entraînent, évaluent, sauvegardent et utilisent le modèle de prédiction. 
Le projet utilise un arbre de décision (DecisionTreeClassifier) provenant de la bibliothèque scikit-learn pour prédire si un client est susceptible de souscrire à un produit bancaire (yes ou no).

1.1. separer_donnees(): 
Divise le jeu de données en 2 ensembles: 80 % pour entraîner le modèle et 20 % pour les tests. Une graine aléatoire fixe et une stratification sont utilisées pour rendre le résultat reporductible er pour conserver la proportions des catégories dans les 2 ensembles.

1.2. creer_reference():
Crée un modèle de référence qui prédit toujours la catégorie majoritaire. Ce modèle sert à comparer les performances de notre arbre de décision (modèle de prédiction)

L'arbre de décision permet de réaliser une classification (apprentissage automatique) à partir des données du fichier. Il apprends des règles à partir des caractéristiques des clients pour ensuite attribuer yes ou no à un  nouveau client. 

1.3. entrainer_modele():
Utilise ColumnTransformer pour sélectionner les colonnes catégorielles et OneHotEncoder pour transformer ces colonnes en variables numériques. Un Pipeline regroupe le prétraitement (colonnes catégorielles transformées) et l'arbre de décision. 

1.4. evaluer_modele():
Calcule l'exactitude du modèle de référence et la compare à celle du modèle de prédiction. L'exactitude est recalculée avec Numpy. 

1.5. sauvegarder_modele(), sauvegarder_metadonnees() et charger_modele(), chager_metadonnees():
Modèle entraîné sauvegardé dans un fichier pkl. avec Joblib et les métadonées sont sauvegardées dans un fichier JSON. 
Un fichier pickle permettera de conserver le modele entrainer et de le reutiliser sans devoir recommencer l'entrainement à chauque lancement.

1.6. predire():
Cette fonction reçoit les caractéristiques d'un nouveau client et renvoi la catégotie ptédite ainsi que la précision de prédiction du yes et no. 

1.7. preparer_modele():
Regroupe les principales étapes: chargement, nettoyage, séparation, entraînement, évaluation et sauvegarde du modèle. 

2. Vérification du fonctionnement du modele: Test_model.py 
Ce fichier contient les tests qui permettent de véfifier le fonctionnement des fonctions dans modele.py. 
La bibliothèque pytest et un petit jeu de données ont été crées pour effectuer les test sans avoir à utiliser le fichier csv. au complet à chaque test. 

2.1. test_separer_donnees(): 
Vérifie que les données sont correctement divisées entre l'entrainement et les test. 

2.2. test_creer_reference():
Vérifie que le modele de reference predit la classe majoritaire

2.3. test_entrainer_modele():
Vérifie que le modele peut être entrainé et que les predictions sont valides

2.4. test_evaluer_modele():
Vérifie que les métriques sont calculées correctement et que l'exactitude calculée avec Numpy correspond à celle calculée avec scikit-learn

2.5. test_sauvegarder_et_charger_modele():
Vérifie que le modele peut être sauvegardé et rechargé correctement.

2.6. test_charger_modele_fichier_absent():
Vérifie le comportement quand le fichier est introuvable.

2.7. test_sauvegarder_et_charger_metadonnees
Vérifie que les métadonnées peuvent être sauvegardées et rechargées correctement.

2.8. test_charger_metadonnees_fichier_absent():
Vérifie le comportement quand le fichier des métadonnées est introuvable.

2.9. test_predire():
Vérifie que la fonction de prédiction retourne une catégorie valide et deux probabilités entre 0 et 1 (somme = 1)

Les test se font avec la commande : python3 -m pytest -v

3. Interface graphique : interface.py
Ce fichier contient la classe Application, qui construit l'interface graphique du projet avec la bibliothèque Tkinter. Il perment à l'utilisateur d'intéragir avec le modèle. 

3.1. __init__():
Initialise la fenêtre principale (titre et dimension) et organise les éléments graphiques et les champs de saisie. Les champs de saisie sont construits à partir de la liste des variables reçues par l'application. Les variables numériques utilisent des champs de saisie et les variables catégorielles utilisent des listes déroulentes.

3.2. faire_prediction():
Récupère les valeurs saisies, vérifie leur validité et les regroupe dans un DataFrame pandas. Les données sont transmises à la fonction predire() de model.py

3.3. enregistrer_prediction():
Crée un fichier csv contenant l'historique des prédictions (caractéristiques, prédictions et probabilités)

3.4. creer_graphique():
Crée le grapihique Matplotlib intégré à l'interface pour représenter les résultats des prédictions.

3.5. mettre_a_jour_grahique(): 
Actualise le graphique quand de nouvelles prédictions sont effectuées. 

3.6. lancer():
Démarre la boucle principale de Tkinter (mainloop()) pour que l,utilisateur intéragisse avec l'interface.

>>>>>>> cfceb63f9fdb3ea46576b59cf0b3dd48ac257013
