
class TableDesSymboles:
    def __init__(self):
        self.fonctions = {}  
        self.variables = {}  
        self.contexte_fonction = None  
    
    def ajouter_fonction(self, nom, type_retour):
        
        if nom in self.fonctions:
            raise Exception(f"Erreur: fonction '{nom}' déjà définie")
        self.fonctions[nom] = type_retour
    
    def obtenir_type_fonction(self, nom):
        
        if nom not in self.fonctions:
            raise Exception(f"Erreur: fonction '{nom}' non définie")
        return self.fonctions[nom]



    def fonction_existe(self, nom):
        
        return nom in self.fonctions


    
    def entrer_contexte_fonction(self, nom):
        
        self.contexte_fonction = nom


    
    def sortir_contexte_fonction(self):
        
        self.contexte_fonction = None


    
    def est_dans_fonction(self):
        

        return self.contexte_fonction is not None


    
    def obtenir_type_fonction_courante(self):
        
        if self.contexte_fonction is None:
            raise Exception("Erreur: pas dans une fonction")
        return self.fonctions[self.contexte_fonction]    
    
    
    
    def afficher(self):
        """
        Affiche la table des symboles (pour debug)
        """
        print("=== Table des symboles ===")
        print("Fonctions:")
        for nom, type_retour in self.fonctions.items():
            print(f"  {nom}: {type_retour}")
        print("==========================")