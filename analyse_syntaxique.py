import sys
from sly import Parser
from analyse_lexicale import FloLexer
import arbre_abstrait

class FloParser(Parser):
    tokens = FloLexer.tokens

    precedence = (
        ('left', 'OU'),
        ('left', 'ET'),
        ('right', 'NON'),
        ('left', 'EGAL', 'DIFFERENT'),
        ('left', 'INFERIEUR', 'INFERIEUR_OU_EGAL', 'SUPERIEUR', 'SUPERIEUR_OU_EGAL'),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', 'UMINUS'),
    )

    expected_shift_reduce = 0

    @_('listeFonctions listeInstructions')
    def prog(self, p):
        return arbre_abstrait.Programme(p.listeFonctions, p.listeInstructions)

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

    @_('TYPE_ENTIER')
    def TYPE(self, p):
        return 'entier'

    @_('TYPE_BOOLEEN')
    def TYPE(self, p):
        return 'booleen'

    @_('instruction')
    def listeInstructions(self, p):
        l = arbre_abstrait.ListeInstructions()
        l.instructions.append(p[0])
        return l

    @_('instruction listeInstructions')
    def listeInstructions(self, p):
        p.listeInstructions.instructions.insert(0, p.instruction)
        return p.listeInstructions

    @_('ecrire')
    def instruction(self, p):
        return p[0]

    @_('IDENTIFIANT AFFECTATION expression ";"')
    def instruction(self, p):
        return arbre_abstrait.Affectation(p.IDENTIFIANT, p.expression)

    @_('TYPE IDENTIFIANT ";"')
    def instruction(self, p):
        return arbre_abstrait.Declaration(p.TYPE, p.IDENTIFIANT)

    @_('TYPE IDENTIFIANT AFFECTATION expression ";"')
    def instruction(self, p):
        return arbre_abstrait.DeclarationAffectation(p.TYPE, p.IDENTIFIANT, p.expression)

    @_('SI "(" expression ")" "{" listeInstructions "}" liste_elif_else')
    def instruction(self, p):
        si_node = arbre_abstrait.Si(p.expression, p.listeInstructions)
        si_node.corps_sinon_si = p.liste_elif_else[0]
        si_node.corps_sinon = p.liste_elif_else[1]
        return si_node

    @_('TANTQUE "(" expression ")" "{" listeInstructions "}"')
    def instruction(self, p):
        return arbre_abstrait.Tantque(p.expression, p.listeInstructions)

    @_('RETOURNER expression ";"')
    def instruction(self, p):
        return arbre_abstrait.Retourner(p.expression)

    @_('IDENTIFIANT "(" listeArguments ")" ";"')
    def instruction(self, p):
        return arbre_abstrait.AppelFonctionInstruction(p.IDENTIFIANT, p.listeArguments)

    @_('ECRIRE "(" expression ")" ";"')
    def ecrire(self, p):
        return arbre_abstrait.Ecrire(p.expression)

    @_('disjonction')
    def expression(self, p):
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

    @_('addition')
    def comparaison(self, p):
        return p.addition

    @_('addition EGAL addition')
    def comparaison(self, p):
        return arbre_abstrait.Operation('==', p[0], p[2])

    @_('addition DIFFERENT addition')
    def comparaison(self, p):
        return arbre_abstrait.Operation('!=', p[0], p[2])

    @_('addition INFERIEUR addition')
    def comparaison(self, p):
        return arbre_abstrait.Operation('<', p[0], p[2])

    @_('addition INFERIEUR_OU_EGAL addition')
    def comparaison(self, p):
        return arbre_abstrait.Operation('<=', p[0], p[2])

    @_('addition SUPERIEUR addition')
    def comparaison(self, p):
        return arbre_abstrait.Operation('>', p[0], p[2])

    @_('addition SUPERIEUR_OU_EGAL addition')
    def comparaison(self, p):
        return arbre_abstrait.Operation('>=', p[0], p[2])

    @_('multiplication')
    def addition(self, p):
        return p.multiplication

    @_('addition "+" multiplication')
    def addition(self, p):
        return arbre_abstrait.Operation('+', p.addition, p.multiplication)

    @_('addition "-" multiplication')
    def addition(self, p):
        return arbre_abstrait.Operation('-', p.addition, p.multiplication)

    @_('facteur')
    def multiplication(self, p):
        return p.facteur

    @_('multiplication "*" facteur')
    def multiplication(self, p):
        return arbre_abstrait.Operation('*', p.multiplication, p.facteur)

    @_('multiplication "/" facteur')
    def multiplication(self, p):
        return arbre_abstrait.Operation('/', p.multiplication, p.facteur)

    @_('multiplication "%" facteur')
    def multiplication(self, p):
        return arbre_abstrait.Operation('%', p.multiplication, p.facteur)

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

    @_('"(" expression ")"')
    def facteur(self, p):
        return p.expression

    @_('"-" facteur %prec UMINUS')
    def facteur(self, p):
        return arbre_abstrait.Operation('-', arbre_abstrait.Entier(0), p.facteur)

    @_('')
    def listeArguments(self, p):
        return []

    @_('expression')
    def listeArguments(self, p):
        return [p.expression]

    @_('expression "," listeArguments')
    def listeArguments(self, p):
        return [p.expression] + p.listeArguments

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

    @_('SINON_SI "(" expression ")" "{" listeInstructions "}"')
    def elif_block(self, p):
        return arbre_abstrait.Elif(p.expression, p.listeInstructions)

    @_('SINON "{" listeInstructions "}"')
    def else_block(self, p):
        return arbre_abstrait.Else(p.listeInstructions)

    def error(self, p):
        print('Erreur de syntaxe', p, file=sys.stderr)
        exit(1)

if __name__ == '__main__':
    lexer = FloLexer()
    parser = FloParser()
    if len(sys.argv) < 2:
        print("usage: python3 analyse_syntaxique.py NOM_FICHIER_SOURCE.flo")
    else:
        with open(sys.argv[1], "r") as f:
            data = f.read()
            try:
                arbre = parser.parse(lexer.tokenize(data))
                arbre.afficher()
            except EOFError:
                exit(1)
