# table_des_symboles.py

class TableDesSymboles:
    def __init__(self):
        self.fonctions = {}
        self.variables = {}
        self.contexte_fonction = None
        self.profondeur = 0
        self.pile_contextes = []
        self.offset_variables = -4

    def ajouter_fonction(self, nom, type_retour, parametres=None):
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
        if nom not in self.fonctions:
            raise Exception(f"Erreur: fonction '{nom}' non définie")
        return self.fonctions[nom]['type_retour']

    def fonction_existe(self, nom):
        return nom in self.fonctions

    def verifier_appel_fonction(self, nom, arguments):
        if nom not in self.fonctions:
            raise Exception(f"Erreur: fonction '{nom}' non définie")
        fonction = self.fonctions[nom]
        if len(arguments) != fonction['nb_parametres']:
            raise Exception(f"Erreur: fonction '{nom}' attend {fonction['nb_parametres']} arguments, {len(arguments)} fournis")
        return fonction['type_retour']

    def entrer_contexte_fonction(self, nom):
        if nom not in self.fonctions:
            raise Exception(f"Erreur: fonction '{nom}' non définie")
        self.contexte_fonction = nom
        self.profondeur = 0
        self.variables = {}
        self.offset_variables = -4

    def sortir_contexte_fonction(self):
        self.contexte_fonction = None
        self.profondeur = 0
        self.variables = {}
        self.offset_variables = -4

    def est_dans_fonction(self):
        return self.contexte_fonction is not None

    def obtenir_type_fonction_courante(self):
        if self.contexte_fonction is None:
            raise Exception("Erreur: pas dans une fonction")
        return self.fonctions[self.contexte_fonction]['type_retour']

    def entrer_bloc(self):
        self.profondeur += 1

    def sortir_bloc(self):
        if self.profondeur > 0:
            to_remove = []
            for nom, info in self.variables.items():
                if info.get('profondeur', 0) == self.profondeur:
                    to_remove.append(nom)
            for nom in to_remove:
                del self.variables[nom]
            self.profondeur -= 1

    def ajouter_variable(self, nom, type_var, adresse=None):
        if nom in self.variables:
            info_var = self.variables[nom]
            if info_var.get('profondeur', 0) == self.profondeur and info_var.get('fonction', None) == self.contexte_fonction:
                raise Exception(f"Erreur: variable '{nom}' déjà définie dans ce contexte")
        if adresse is None:
            adresse = self.offset_variables
            self.offset_variables -= 4
        self.variables[nom] = {
            'type': type_var,
            'adresse': adresse,
            'profondeur': self.profondeur,
            'fonction': self.contexte_fonction
        }

    def obtenir_variable(self, nom):
        if nom not in self.variables:
            raise Exception(f"Erreur: variable '{nom}' non définie")
        return self.variables[nom]

    def variable_existe(self, nom):
        return nom in self.variables

    def obtenir_parametres_fonction(self, nom):
        if nom not in self.fonctions:
            raise Exception(f"Erreur: fonction '{nom}' non définie")
        return self.fonctions[nom]['parametres']

    def obtenir_memoire_parametres(self, nom):
        if nom not in self.fonctions:
            raise Exception(f"Erreur: fonction '{nom}' non définie")
        return self.fonctions[nom]['memoire_parametres']

    def afficher(self):
        print("=== Table des symboles ===")
        print("Fonctions:")
        for nom, info in self.fonctions.items():
            params = info['parametres']
            if params:
                params_str = ", ".join([f"{t} {n}" for t, n in params])
                print(f"  {nom}({params_str}): {info['type_retour']} - {info['memoire_parametres']} octets")
            else:
                print(f"  {nom}(): {info['type_retour']} - 0 octets")
        print("Variables:")
        if self.variables:
            for nom, info in self.variables.items():
                print(f"  {nom}: {info['type']} @ {info['adresse']} (profondeur: {info.get('profondeur', 0)}, fonction: {info.get('fonction', 'global')})")
        else:
            print("  Aucune variable définie")
        print("==========================")

    def reset(self):
        self.fonctions = {}
        self.variables = {}
        self.contexte_fonction = None
        self.profondeur = 0
        self.pile_contextes = []
        self.offset_variables = -4
