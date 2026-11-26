Pour l'utilisation de l'ia , ma coequipiere et moi avons utilisé l' IA comme assistance c'est à dire que là où on etait bloqué on demandait son aide pour ma part j'ai utilisé claude ai et ma cooequipiere chatgpt. 
# outil | questions |reponses |verifications |decisions 
claude ai | lire le csv et retrourner le dataframe |  if not os.path.exists(chemin):
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    with open(chemin, encoding="utf-8") as fichier:
        return pd.read_csv(fichier, sep=";") |verifications correctes | bonne prise 


chat gpt | comment ameliorer la performance du modele | equilibre son apprentissage avec class/weight = "balance"|