import sys
from sly import Parser
from analyse_lexicale import FloLexer
import arbre_abstrait

class FloParser(Parser):
    tokens = FloLexer.tokens

    # Programme
    @_('listeFonctions listeInstructions')
    @_('listeFonctions')
    def prog(self, p):
        # Si on a seulement listeFonctions (longueur p == 1), pas d’instructions globales
        if hasattr(p, 'listeInstructions'):
            return arbre_abstrait.Programme(p.listeFonctions, p.listeInstructions)
        else:
            return arbre_abstrait.Programme(p.listeFonctions,
                                            arbre_abstrait.ListeInstructions())

    # Liste de fonctions (peut être vide)
    @_('')
    def listeFonctions(self, p):
        return arbre_abstrait.ListeFonctions()

    @_('fonction listeFonctions')
    def listeFonctions(self, p):
        p.listeFonctions.fonctions.insert(0, p.fonction)
        return p.listeFonctions

    @_('TYPE IDENTIFIANT "(" listeParametres ")" "{" listeInstructions "}"')
    def fonction(self, p):
        return arbre_abstrait.Fonction(p.TYPE, p.IDENTIFIANT,
                                       p.listeParametres, p.listeInstructions)

    # Paramètres de fonction (peut être vide)
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

    # Liste d'instructions (au moins une)
    @_('instruction')
    @_('instruction listeInstructions')
    def listeInstructions(self, p):
        if len(p) == 2:
            p[1].instructions.insert(0, p.instruction)
            return p[1]
        l = arbre_abstrait.ListeInstructions()
        l.instructions.append(p.instruction)
        return l

    # Instructions
    @_('ECRIRE "(" expression ")" ";"')
    def ecrire(self, p):
        return arbre_abstrait.Ecrire(p.expression)

    @_('ecrire')
    def instruction(self, p):
        return p.ecrire

    @_('IDENTIFIANT AFFECTATION expression ";"')
    def instruction(self, p):
        return arbre_abstrait.Affectation(p.IDENTIFIANT, p.expression)

    # Déclaration (avec ou sans initialisation)
    @_('TYPE IDENTIFIANT opt_init ";"')
    def instruction(self, p):
        if p.opt_init is None:
            return arbre_abstrait.Declaration(p.TYPE, p.IDENTIFIANT)
        else:
            return arbre_abstrait.DeclarationAffectation(p.TYPE,
                                                        p.IDENTIFIANT,
                                                        p.opt_init)

    @_('AFFECTATION expression')
    def opt_init(self, p):
        return p.expression

    @_('')
    def opt_init(self, p):
        return None

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
        return arbre_abstrait.AppelFonctionInstruction(p.IDENTIFIANT,
                                                       p.listeArguments)

    # Arguments d'appel (peuvent être vides)
    @_('')
    def listeArguments(self, p):
        return []

    @_('expression')
    def listeArguments(self, p):
        return [p.expression]

    @_('expression "," listeArguments')
    def listeArguments(self, p):
        return [p.expression] + p.listeArguments

    # Bloc elif / else
    @_('liste_elif else_block')
    @_('liste_elif')
    @_('else_block')
    @_('')
    def liste_elif_else(self, p):
        if len(p) == 2 and isinstance(p[0], list):
            return (p[0], p[1])
        if len(p) == 1 and isinstance(p[0], list):
            return (p[0], None)
        if len(p) == 1 and isinstance(p[0], arbre_abstrait.Else):
            return ([], p[0])
        return ([], None)

    @_('liste_elif elif_block')
    @_('elif_block')
    def liste_elif(self, p):
        if len(p) == 1:
            return [p.elif_block]
        p.liste_elif.append(p.elif_block)
        return p.liste_elif

    @_('SINON_SI "(" expression ")" "{" listeInstructions "}"')
    def elif_block(self, p):
        return arbre_abstrait.Elif(p.expression, p.listeInstructions)

    @_('SINON "{" listeInstructions "}"')
    def else_block(self, p):
        return arbre_abstrait.Else(p.listeInstructions)

    # ——— Expressions ———
    @_('or_expr')
    def expression(self, p):
        return p.or_expr

    @_('or_expr OU and_expr')
    def or_expr(self, p):
        return arbre_abstrait.Operation('ou', p.or_expr, p.and_expr)

    @_('and_expr')
    def or_expr(self, p):
        return p.and_expr

    @_('and_expr ET neg_expr')
    def and_expr(self, p):
        return arbre_abstrait.Operation('et', p.and_expr, p.neg_expr)

    @_('neg_expr')
    def and_expr(self, p):
        return p.neg_expr

    @_('NON neg_expr')
    def neg_expr(self, p):
        return arbre_abstrait.Operation('non', p.neg_expr, None)

    @_('cmp_expr')
    def neg_expr(self, p):
        return p.cmp_expr

    @_('add_expr')
    @_('add_expr EGAL add_expr')
    @_('add_expr DIFFERENT add_expr')
    @_('add_expr INFERIEUR add_expr')
    @_('add_expr INFERIEUR_OU_EGAL add_expr')
    @_('add_expr SUPERIEUR add_expr')
    @_('add_expr SUPERIEUR_OU_EGAL add_expr')
    def cmp_expr(self, p):
        if len(p) == 1:
            return p.add_expr
        return arbre_abstrait.Operation(p[1], p[0], p[2])

    @_('add_expr "+" mul_expr')
    @_('add_expr "-" mul_expr')
    @_('mul_expr')
    def add_expr(self, p):
        if len(p) == 1:
            return p.mul_expr
        return arbre_abstrait.Operation(p[1], p[0], p[2])

    @_('mul_expr "*" unary')
    @_('mul_expr "/" unary')
    @_('mul_expr "%" unary')
    @_('unary')
    def mul_expr(self, p):
        if len(p) == 1:
            return p.unary
        return arbre_abstrait.Operation(p[1], p[0], p[2])

    @_('"-" unary')
    @_('primary')
    def unary(self, p):
        if len(p) == 1:
            return p.primary
        return arbre_abstrait.Operation('-', arbre_abstrait.Entier(0), p.unary)

    @_('ENTIER')
    def primary(self, p):
        return arbre_abstrait.Entier(p.ENTIER)

    @_('BOOLEEN')
    def primary(self, p):
        return arbre_abstrait.Booleen(p.BOOLEEN)

    @_('LIRE "(" ")"')
    def primary(self, p):
        return arbre_abstrait.Lire()

    @_('IDENTIFIANT "(" listeArguments ")"')
    def primary(self, p):
        return arbre_abstrait.AppelFonction(p.IDENTIFIANT, p.listeArguments)

    @_('IDENTIFIANT')
    def primary(self, p):
        return arbre_abstrait.Variable(p.IDENTIFIANT)

    @_('"(" expression ")"')
    def primary(self, p):
        return p.expression

    # Gestion des erreurs
    def error(self, p):
        if p:
            print(f"Erreur de syntaxe ligne {p.lineno} : symbole inattendu '{p.value}'", file=sys.stderr)
        else:
            print("Erreur de syntaxe en fin de fichier", file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    lexer  = FloLexer()
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
