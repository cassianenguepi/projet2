Prédiction de souscription à un produit bancaire

1. Description du projet:
Ce projet consiste à prédire si un client est susceptible de souscrire à un produit bancaire à la suite d'une campagne de marketing téléphonique. Le modèle de prédition utilise un arbre de décision qui permet unn apprentissage automatique à partir des données du fichier de données. L'utilisateur peut saisir les caractérisiques demandées dans une interface graphique et obtenir une prédiction et les probabilités associées à cette probabilité. 

2. Prétraitement des données: 
Avant l'entrainement, les doublons ont été supprimés du fichier. Ensuite, la variable duration a également été supprimée, car elle représente la durée de l'appelle et cette donnée n'est connue qu'après l'appel. La donnée pdays a été remplacée par deja_contacte, un valeur binaire qui utilise 0 pour non, et 1 pour oui. Fianlement, les variables catégorielles ont été encodées avec le module OneHotEncoder.

3. Installation:
Les modules requis ont été installés à partir du fichier requirements.txt en executant dans le terminal:
    pip install -r requirements.txt

4. Lancement de l'interface:
Afin de lancer l'interface avec laquelle l'utilisateur interagira, il faut executer: 
    python3 -m src.main  #python3 pour macbook

5. Rôle des modules:
    donnees.py: Charge, nettoie et prépare les données. Contient les classes représentant les variables et le jeu de données. 

    exceptions.py: Définie les erreurs afon de gérer les données invalides sans que le programme se termine ou bloque. 

    model.py: Sépare les données, entraîne et évalue le modèle, sauvegarde et charge le modèle et effectue les prédictions.

    interface.py: Contient la classe Application qui construit l'interface graphique. 

    main.py: Prépare les données, charge le modèle et lance l'interface.

6. Modèle et Résultats
Le modèle utilise un arbre de décision (DecisionTreeClassifier) pour prédire les résultats. Les données sont séparées en 2: 80% pour l'entraînement, et 20% pour le test. 
Résultats:
Mesure              Modèle de prédiction            Modèle de référence
Exactitude          84,57 %                         88,73 %

L'excatitude calculée avec Numpy concorde avec celle calculée avec scikit-learn. 

7. Tests:
Utilisation de pytest: python3 -m pytest -v
Pour le rapport de couverture: 
    python3 -m pytest --cov=src --cov-report=term-missing
Ils vérifient le chargement et le nettoyage des données, la validation des données, le fonctionnement du modèle, le calcul des métriques et la gestion des erreurs.

8. Intégration continue
Nous utilisons GitHub Actions pour automatiquement exécuter les tests lors d'un push-pull request.

9. Outil avancé utilisé du chpitre 7:
- Nombre d'argument arbitraire : predire(modele, nouvelles_donnees)
- Fonction comme objet: command=self.faire_prediction
- Portée des variables et espaces de noms: Variables locales dans les fonctions et variables définies au niveau du module (CHEMIN_CSV)
-  Modules: réutiliser les fonctions: main.py réutilise et importe donnees.py et model.py

10. Références:
https://scikit-learn.org/stable/ 
https://docs.pytest.org/en/stable/ 
https://www.w3schools.com/python/python_tkinter.asp 
