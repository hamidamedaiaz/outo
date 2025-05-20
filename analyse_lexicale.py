import sys
from sly import Lexer


class FloLexer(Lexer):
    # Noms des lexèmes (sauf les litéraux). En majuscule. Ordre non important
    tokens = { IDENTIFIANT, ENTIER, ECRIRE, LIRE, INFERIEUR_OU_EGAL, 
    BOOLEEN, EGAL, SUPERIEUR, INFERIEUR, DIFFERENT, RETOURNER, ET, OU, 
    NON, AFFECTATION, TANTQUE, SINON, SI, SUPERIEUR_OU_EGAL, TYPE_BOOLEEN, TYPE_ENTIER, SINON_SI}

    #Les caractères litéraux sont des caractères uniques qui sont retournés tel quel quand rencontré par l'analyse lexicale. 
    #Les litéraux sont vérifiés en dernier, après toutes les autres règles définies par des expressions régulières.
    #Donc, si une règle commence par un de ces littérals (comme INFERIEUR_OU_EGAL), cette règle aura la priorité.
    literals = { '+',"-",'*','(',')',";",",","{","}","[","]","/","%"}
    
    # chaines contenant les caractère à ignorer. Ici espace et tabulation
    ignore = ' \t'

    # Expressions régulières correspondant au différents Lexèmes par ordre de priorité
    INFERIEUR_OU_EGAL= r'<='
    EGAL=r'=='
    SUPERIEUR =r'>'
    INFERIEUR =r'<'
    DIFFERENT =r'!='
    AFFECTATION =r'='
    SUPERIEUR_OU_EGAL=r'>='
    

    
    @_(r'0|[1-9][0-9]*')
    def ENTIER(self, t):
        t.value = int(t.value)
        return t

    @_(r'Vrai|Faux')
    def BOOLEEN(self,t):
        t.value = t.value == 'Vrai'
        return t
    
    @_(r'sinon\s+si')
    def SINON_SI(self, t):
        return t


    @_(r'[a-zA-Z][a-zA-Z0-9_]*')
    def IDENTIFIANT(self, t):
        if t.value == 'et':
            t.type = 'ET'
        elif t.value == 'ou':
            t.type = 'OU'
        elif t.value == 'non':
            t.type = 'NON'
        elif t.value == 'ecrire':
            t.type = 'ECRIRE'
        elif t.value == 'tantque':
            t.type = 'TANTQUE'
        elif t.value == 'sinon':
            t.type ='SINON'
        elif t.value == 'si':
            t.type = 'SI'
        elif t.value =='retourner':
            t.type ='RETOURNER'
        elif t.value == 'lire':
            t.type ='LIRE'
        elif t.value == 'booleen':
            t.type ='TYPE_BOOLEEN'
        elif t.value == 'entier':
            t.type ='TYPE_ENTIER'
        return t
    #Syntaxe des commentaires à ignorer
    ignore_comment = r'\#.*'

    # Permet de conserver les numéros de ligne. Utile pour les messages d'erreurs
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # En cas d'erreur, indique où elle se trouve
    def error(self, t):
        print(f'Ligne{self.lineno}: caractère inattendu "{t.value[0]}"',file=sys.stderr)
        print(f"{t.value}")
        self.index += 1
        exit(1)
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python3 analyse_lexicale.py NOM_FICHIER_SOURCE.flo")
    else:
        with open(sys.argv[1],"r") as f:
            data = f.read()
            lexer = FloLexer()
            for tok in lexer.tokenize(data):
                print(tok)
