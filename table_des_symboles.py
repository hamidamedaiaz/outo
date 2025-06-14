class TableDesSymboles:
    def __init__(self):
        self.fonctions = {}  
        self.variables = {}  
        self.contexte_fonction = None  
        self.profondeur = 0
        self.pile_contextes = []
        self.offset_variables = -4  # Pour les adresses des variables locales
    
    def ajouter_fonction(self, nom, type_retour, parametres=None):
        """
        Ajoute une fonction à la table des symboles
        """
        if nom in self.fonctions:
            raise Exception(f"Erreur: fonction '{nom}' déjà définie")
        
        if parametres is None:
            parametres = []
            
        self.fonctions[nom] = {
            'type_retour': type_retour,
            'parametres': parametres,
            'nb_parametres': len(parametres),
            'memoire_parametres': len(parametres) * 4
        }
    
    def obtenir_type_fonction(self, nom):
        """
        Retourne le type de retour d'une fonction
        """
        if nom not in self.fonctions:
            raise Exception(f"Erreur: fonction '{nom}' non définie")
        return self.fonctions[nom]['type_retour']

    def fonction_existe(self, nom):
        """
        Vérifie si une fonction existe
        """
        return nom in self.fonctions

    def verifier_appel_fonction(self, nom, arguments):
        """
        Vérifie qu'un appel de fonction est valide
        """
        if nom not in self.fonctions:
            raise Exception(f"Erreur: fonction '{nom}' non définie")
        
        fonction = self.fonctions[nom]
        if len(arguments) != fonction['nb_parametres']:
            raise Exception(f"Erreur: fonction '{nom}' attend {fonction['nb_parametres']} arguments, {len(arguments)} fournis")
        
        return fonction['type_retour']

    def entrer_contexte_fonction(self, nom):
        """
        Entre dans le contexte d'une fonction
        """
        if nom not in self.fonctions:
            raise Exception(f"Erreur: fonction '{nom}' non définie")
        self.contexte_fonction = nom
        self.profondeur = 0
        self.variables = {}  # Reset des variables pour la nouvelle fonction
        self.offset_variables = -4

    def sortir_contexte_fonction(self):
        """
        Sort du contexte de fonction
        """
        self.contexte_fonction = None
        self.profondeur = 0
        self.variables = {}
        self.offset_variables = -4

    def est_dans_fonction(self):
        """
        Vérifie si on est dans une fonction
        """
        return self.contexte_fonction is not None

    def obtenir_type_fonction_courante(self):
        """
        Retourne le type de retour de la fonction courante
        """
        if self.contexte_fonction is None:
            raise Exception("Erreur: pas dans une fonction")
        return self.fonctions[self.contexte_fonction]['type_retour']

    def entrer_bloc(self):
        """
        Entre dans un nouveau bloc
        """
        self.profondeur += 1

    def sortir_bloc(self):
        """
        Sort d'un bloc et supprime les variables locales
        """
        if self.profondeur > 0:
            variables_a_supprimer = []
            for nom, info in self.variables.items():
                if info.get('profondeur', 0) == self.profondeur:
                    variables_a_supprimer.append(nom)
            
            for nom in variables_a_supprimer:
                del self.variables[nom]
            
            self.profondeur -= 1

    def ajouter_variable(self, nom, type_var, adresse=None):
        """
        Ajoute une variable à la table des symboles
        """
        # Vérifier si la variable existe déjà dans le contexte courant
        if nom in self.variables:
            info_var = self.variables[nom]
            if info_var.get('profondeur', 0) == self.profondeur:
                raise Exception(f"Erreur: variable '{nom}' déjà définie dans ce contexte")
        
        if adresse is None:
            # Pour les variables locales, utiliser des adresses négatives
            adresse = self.offset_variables
            self.offset_variables -= 4
        
        self.variables[nom] = {
            'type': type_var,
            'adresse': adresse,
            'profondeur': self.profondeur
        }

    def obtenir_variable(self, nom):
        """
        Retourne les informations d'une variable
        """
        if nom not in self.variables:
            raise Exception(f"Erreur: variable '{nom}' non définie")
        return self.variables[nom]

    def variable_existe(self, nom):
        """
        Vérifie si une variable existe
        """
        return nom in self.variables

    def obtenir_parametres_fonction(self, nom):
        """
        Retourne la liste des paramètres d'une fonction
        """
        if nom not in self.fonctions:
            raise Exception(f"Erreur: fonction '{nom}' non définie")
        return self.fonctions[nom]['parametres']

    def obtenir_memoire_parametres(self, nom):
        """
        Retourne la mémoire nécessaire pour les paramètres
        """
        if nom not in self.fonctions:
            raise Exception(f"Erreur: fonction '{nom}' non définie")
        return self.fonctions[nom]['memoire_parametres']
    
    def afficher(self):
        """
        Affiche la table des symboles pour debug
        """
        print("=== Table des symboles ===")
        print("Fonctions:")
        for nom, info in self.fonctions.items():
            if info['parametres']:
                params_str = ", ".join([f"{t} {n}" for t, n in info['parametres']])
                print(f"  {nom}({params_str}): {info['type_retour']} - {info['memoire_parametres']} octets")
            else:
                print(f"  {nom}(): {info['type_retour']} - 0 octets")
        
        print("Variables:")
        if self.variables:
            for nom, info in self.variables.items():
                print(f"  {nom}: {info['type']} @ {info['adresse']} (profondeur: {info.get('profondeur', 0)})")
        else:
            print("  Aucune variable définie")
        print("==========================")

    def reset(self):
        """
        Remet à zéro la table des symboles
        """
        self.fonctions = {}
        self.variables = {}
        self.contexte_fonction = None
        self.profondeur = 0
        self.pile_contextes = []
        self.offset_variables = -4