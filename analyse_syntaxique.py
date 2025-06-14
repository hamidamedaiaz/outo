import sys
from sly import Parser
from analyse_lexicale import FloLexer
import arbre_abstrait

class FloParser(Parser):
    
    tokens = FloLexer.tokens

    # Règles de précédence pour ÉLIMINER TOUS LES CONFLITS
    precedence = (
        ('left', 'OU'),
        ('left', 'ET'),
        ('right', 'NON'),
        ('left', 'EGAL', 'DIFFERENT', 'INFERIEUR', 'INFERIEUR_OU_EGAL', 'SUPERIEUR', 'SUPERIEUR_OU_EGAL'),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', 'UMINUS'),
    )

    # Nombre de conflits attendus - DOIT ÊTRE 0
    expected_shift_reduce = 0

    #-----------------------
    # Programme principal - 2 règles pour gérer avec/sans fonctions
    #-----------------------
    @_('listeFonctions listeInstructions')
    def prog(self, p):
        return arbre_abstrait.Programme(p.listeFonctions, p.listeInstructions)    

    @_('listeInstructions')
    def prog(self, p):
        return arbre_abstrait.Programme(arbre_abstrait.ListeFonctions(), p.listeInstructions)

    #------------------------------------------
    # Fonctions
    #------------------------------------------
    @_('')
    def listeFonctions(self, p):
        return arbre_abstrait.ListeFonctions()

    @_('fonction listeFonctions')
    def listeFonctions(self, p):
        p.listeFonctions.fonctions.insert(0, p.fonction)
        return p.listeFonctions

    @_('TYPE IDENTIFIANT "(" listeParametres ")" "{" listeInstructions "}"')
    def fonction(self, p):
        return arbre_abstrait.Fonction(p.TYPE, p.IDENTIFIANT, p.listeParametres, p.listeInstructions)

    @_('')
    def listeParametres(self, p):
        return arbre_abstrait.ListeParametres()

    @_('parametre')
    def listeParametres(self, p):
        l = arbre_abstrait.ListeParametres()
        l.parametres.append(p.parametre)
        return l

    @_('parametre "," listeParametres')
    def listeParametres(self, p):
        p.listeParametres.parametres.insert(0, p.parametre)
        return p.listeParametres

    @_('TYPE IDENTIFIANT')
    def parametre(self, p):
        return arbre_abstrait.Parametre(p.TYPE, p.IDENTIFIANT)

    #---------------------
    # Types
    #---------------------
    @_('TYPE_ENTIER')
    def TYPE(self, p):
        return 'entier'

    @_('TYPE_BOOLEEN')
    def TYPE(self, p):
        return 'booleen'

    #---------------------
    # Instructions
    #---------------------         
    @_('instruction')
    def listeInstructions(self, p):
        l = arbre_abstrait.ListeInstructions()
        l.instructions.append(p[0])
        return l
                    
    @_('instruction listeInstructions')
    def listeInstructions(self, p):
        p[1].instructions.insert(0,p[0])
        return p[1]
        
    @_('ecrire')
    def instruction(self, p):
        return p[0]

    @_('IDENTIFIANT AFFECTATION expr ";"')
    def instruction(self, p):
        return arbre_abstrait.Affectation(p.IDENTIFIANT, p.expr)

    @_('TYPE IDENTIFIANT ";"')
    def instruction(self,p):
        return arbre_abstrait.Declaration(p.TYPE, p.IDENTIFIANT)
    
    @_('TYPE IDENTIFIANT AFFECTATION expr ";"')
    def instruction(self,p):
        return arbre_abstrait.DeclarationAffectation(p.TYPE, p.IDENTIFIANT, p.expr)

    @_('SI "(" expr ")" "{" listeInstructions "}" liste_elif_else')
    def instruction(self, p):
        si_node = arbre_abstrait.Si(p.expr, p.listeInstructions)
        si_node.corps_sinon_si = p.liste_elif_else[0]
        si_node.corps_sinon = p.liste_elif_else[1]
        return si_node
    
    @_('TANTQUE "(" expr ")" "{" listeInstructions "}"')
    def instruction(self, p):
        return arbre_abstrait.Tantque(p.expr, p.listeInstructions)

    @_('RETOURNER expr ";"')
    def instruction(self, p):
        return arbre_abstrait.Retourner(p.expr)

    @_('IDENTIFIANT "(" listeArguments ")" ";"')
    def instruction(self, p):
        return arbre_abstrait.AppelFonctionInstruction(p.IDENTIFIANT, p.listeArguments)
            
    @_('ECRIRE "(" expr ")" ";"')
    def ecrire(self, p):
        return arbre_abstrait.Ecrire(p.expr) 

    #---------------------
    # Expressions - CASCADE STRICTE pour éviter les conflits
    #---------------------
    @_('disjonction')
    def expr(self, p):
        return p.disjonction

    @_('conjonction')
    def disjonction(self, p):
        return p.conjonction

    @_('disjonction OU conjonction')
    def disjonction(self, p):
        return arbre_abstrait.Operation('ou', p.disjonction, p.conjonction)

    @_('negation')
    def conjonction(self, p):
        return p.negation

    @_('conjonction ET negation')
    def conjonction(self, p):
        return arbre_abstrait.Operation('et', p.conjonction, p.negation)

    @_('comparaison')
    def negation(self, p):
        return p.comparaison

    @_('NON negation')
    def negation(self, p):
        return arbre_abstrait.Operation('non', p.negation, None)

    @_('somme')
    def comparaison(self, p):
        return p.somme

    @_('somme EGAL somme')
    def comparaison(self, p):
        return arbre_abstrait.Operation('==', p[0], p[2])

    @_('somme DIFFERENT somme')
    def comparaison(self, p):
        return arbre_abstrait.Operation('!=', p[0], p[2])

    @_('somme INFERIEUR somme')
    def comparaison(self, p):
        return arbre_abstrait.Operation('<', p[0], p[2])

    @_('somme INFERIEUR_OU_EGAL somme')
    def comparaison(self, p):
        return arbre_abstrait.Operation('<=', p[0], p[2])

    @_('somme SUPERIEUR somme')
    def comparaison(self, p):
        return arbre_abstrait.Operation('>', p[0], p[2])

    @_('somme SUPERIEUR_OU_EGAL somme')
    def comparaison(self, p):
        return arbre_abstrait.Operation('>=', p[0], p[2])
    
    @_('produit')
    def somme(self, p):
        return p.produit

    @_('somme "+" produit')
    def somme(self, p):
        return arbre_abstrait.Operation('+', p[0], p[2])

    @_('somme "-" produit')
    def somme(self, p):
        return arbre_abstrait.Operation('-', p[0], p[2])

    @_('facteur')
    def produit(self, p):
        return p.facteur

    @_('produit "*" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('*', p[0], p[2])

    @_('produit "/" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('/', p[0], p[2])

    @_('produit "%" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('%', p[0], p[2])

    #---------------------
    # Facteurs - ordre important pour éviter les conflits
    #---------------------
    @_('ENTIER')
    def facteur(self, p):
        return arbre_abstrait.Entier(p.ENTIER) 
    
    @_('BOOLEEN')
    def facteur(self, p):
        return arbre_abstrait.Booleen(p.BOOLEEN)

    @_('LIRE "(" ")"')
    def facteur(self, p):
        return arbre_abstrait.Lire()

    @_('IDENTIFIANT "(" listeArguments ")"')
    def facteur(self, p):
        return arbre_abstrait.AppelFonction(p.IDENTIFIANT, p.listeArguments)

    @_('IDENTIFIANT')
    def facteur(self, p):
        return arbre_abstrait.Variable(p.IDENTIFIANT)

    @_('"(" expr ")"')
    def facteur(self, p):
        return p.expr

    @_('"-" facteur %prec UMINUS')
    def facteur(self, p):
        return arbre_abstrait.Operation('-', arbre_abstrait.Entier(0), p[1])

    #---------------------
    # Arguments - version SANS CONFLITS
    #---------------------
    @_('')
    def listeArguments(self, p):
        return []

    @_('expr')
    def listeArguments(self, p):
        return [p.expr]

    @_('expr "," listeArguments')
    def listeArguments(self, p):
        return [p.expr] + p.listeArguments

    #---------------------
    # Si/sinon si/sinon
    #---------------------
    @_('liste_elif else_block')
    def liste_elif_else(self, p):
        return (p.liste_elif, p.else_block)

    @_('liste_elif')
    def liste_elif_else(self, p):
        return (p.liste_elif, None)

    @_('else_block')
    def liste_elif_else(self, p):
        return ([], p.else_block)

    @_('')
    def liste_elif_else(self, p):
        return ([], None)

    @_('elif_block')
    def liste_elif(self, p):
        return [p.elif_block]

    @_('liste_elif elif_block')
    def liste_elif(self, p):
        p.liste_elif.append(p.elif_block)
        return p.liste_elif

    @_('SINON_SI "(" expr ")" "{" listeInstructions "}"')
    def elif_block(self, p):
        return arbre_abstrait.Elif(p.expr, p.listeInstructions)

    @_('SINON "{" listeInstructions "}"')
    def else_block(self, p):
        return arbre_abstrait.Else(p.listeInstructions)

    def error(self, p):
        print('Erreur de syntaxe',p,file=sys.stderr)
        exit(1)

if __name__ == '__main__':
    lexer = FloLexer()
    parser = FloParser()
    if len(sys.argv) < 2:
        print("usage: python3 analyse_syntaxique.py NOM_FICHIER_SOURCE.flo")
    else:
        with open(sys.argv[1],"r") as f:
            data = f.read()
            try:
                arbre = parser.parse(lexer.tokenize(data))
                arbre.afficher()
            except EOFError:
                exit(1)