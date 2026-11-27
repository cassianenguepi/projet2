Pour l'utilisation de l'ia , ma coequipiere et moi avons utilisé l' IA comme assistance c'est à dire que là où on etait bloqué on demandait son aide pour ma part j'ai utilisé claude ai et ma cooequipiere chatgpt. 
# outil | questions |reponses |verifications |decisions 
claude ai | lire le csv et retrourner le dataframe |  if not os.path.exists(chemin):
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    with open(chemin, encoding="utf-8") as fichier:
        return pd.read_csv(fichier, sep=";") |verifications correctes | bonne prise 


chat gpt | comment ameliorer la performance du modele | equilibre son apprentissage avec class_weight = "balanced"|python3 -c "from.src.model import.preparer_modele; print(preparer_modele())"

claude | comment choisir le meilleur fichier csv | aller sur kaggle et decris le fichier que tu veux | site kaggle | prediction d'une souscription dans une banque 

chatgpt| comment faire pour debuter le projet|commencer par subdiviser votre travail en sous fichiers |okay c'est correcte |creation des fichiers donnees.py,exceptions.py,interface.py,main.py,model.py,test_data.py,test_model.py

claude | comment avoir une bonne prediction et surtout que l'interface marche | faire ton main et ajoute la commande pour demarrer| accepter| if __name__ == "__main__":
    main()

claude | explique moi comment faire le fichier donnees.py|indication|validee| production du fichier csv 
 chatgpt| comment utiliser le module tkinter |Tkinter est le module Python standard qui permet de créer des interfaces graphiques (GUI) pour vos applications, en s’appuyant sur le toolkit Tcl/Tk.| c'est correcte | on l'utilise 

 claude| comment faire pour telecharger ou pour importer les modules necessaires pour le travail | utilise pip.install et ajoute le module que tu veux | pip install.requirements | installer les modules necessaire 

 chatgpt| comment test_model.py doit fonctionner | verifie automatiquement que modele.py fonctionne normalement | tous les tests fonctionne et verifie si modele.py fonctionne donc c'est correcte | l'utiliser 

 