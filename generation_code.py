import sys
from analyse_lexicale import FloLexer
from analyse_syntaxique import FloParser
import arbre_abstrait
from table_des_symboles import TableDesSymboles

num_etiquette_courante = -1 
afficher_table = False
afficher_code = False

# Variable globale pour la table des symboles - IMPORTANT
table_symboles = None

def erreur(s):
    print("Erreur:",s,file=sys.stderr)
    exit(1)
    
def printifm(*args,**kwargs):
    if afficher_code:
        print(*args,**kwargs)

def printift(*args,**kwargs):
    if afficher_table:
        print(*args,**kwargs)

def arm_comment(comment):
    if comment != "":
        printifm("\t\t @ "+comment)
    else:
        printifm("")  

def arm_instruction(opcode, op1="", op2="", op3="", comment=""):
    if op2 == "":
        printifm("\t"+opcode+"\t"+op1+"\t\t",end="")
    elif op3 =="":
        printifm("\t"+opcode+"\t"+op1+",\t"+op2+"\t",end="")
    else:
        printifm("\t"+opcode+"\t"+op1+",\t"+op2+",\t"+op3,end="")
    arm_comment(comment)

def arm_nouvelle_etiquette():
    global num_etiquette_courante
    num_etiquette_courante+=1
    return "e"+str(num_etiquette_courante)

def gen_programme(programme):
    global table_symboles
    
    # INITIALISATION OBLIGATOIRE de la table des symboles
    table_symboles = TableDesSymboles()
    
    header=""".LC0:
    .ascii	"%d\\000"
    .align	2
.LC1:
    .ascii	"%d\\012\\000"
    .text
    .align	2
    .global	main
    .global __aeabi_idiv
    .global __aeabi_idivmod"""
    printifm(header)
    
    # Ajouter toutes les fonctions à la table des symboles
    for fonction in programme.listeFonctions.fonctions:
        parametres = [(param.type_param, param.nom) for param in fonction.parametres.parametres]
        table_symboles.ajouter_fonction(fonction.nom, fonction.type_retour, parametres)
    
    if afficher_table:
        table_symboles.afficher()
        return
    
    # Générer le code pour chaque fonction
    for fonction in programme.listeFonctions.fonctions:
        gen_fonction(fonction)
    
    # Code principal - SEULEMENT s'il y a des instructions principales
    if programme.listeInstructions.instructions:
        printifm('main:')
        arm_instruction("push", "{fp,lr}", "", "", "")
        arm_instruction("add", "fp","sp", "#4", "")
        gen_listeInstructions(programme.listeInstructions)
        arm_instruction("mov", "r0", "#0", "", "")
        arm_instruction("pop", "{fp, pc}","","","")
    else:
        # S'il n'y a pas d'instructions principales, créer un main vide
        printifm('main:')
        arm_instruction("push", "{fp,lr}", "", "", "")
        arm_instruction("add", "fp","sp", "#4", "")
        arm_instruction("mov", "r0", "#0", "", "")
        arm_instruction("pop", "{fp, pc}","","","")

def gen_fonction(fonction):
    global table_symboles
    
    table_symboles.entrer_contexte_fonction(fonction.nom)
    
    printifm(f"_{fonction.nom}:")
    arm_instruction("push", "{fp,lr}", "", "", "prologue fonction")
    arm_instruction("add", "fp", "sp", "#4", "")
    
    # Ajouter les paramètres comme variables
    for i, param in enumerate(fonction.parametres.parametres):
        adresse = (len(fonction.parametres.parametres) - i) * 4
        table_symboles.ajouter_variable(param.nom, param.type_param, adresse)
    
    gen_listeInstructions(fonction.corps)
    
    # Retour par défaut
    if fonction.type_retour == 'entier':
        arm_instruction("mov", "r2", "#0", "", "retour par défaut")
    else:
        arm_instruction("mov", "r2", "#0", "", "retour par défaut (Faux)")
    
    arm_instruction("pop", "{fp,pc}", "", "", "épilogue fonction")
    table_symboles.sortir_contexte_fonction()

def gen_listeInstructions(listeInstructions):
    for instruction in listeInstructions.instructions:
        gen_instruction(instruction)

def gen_instruction(instruction):
    if type(instruction) == arbre_abstrait.Ecrire:
        gen_ecrire(instruction)
    elif type(instruction) == arbre_abstrait.Tantque: 
        gen_tantque(instruction)
    elif type(instruction) == arbre_abstrait.Si:  
        gen_si(instruction)
    elif type(instruction) == arbre_abstrait.Affectation: 
        gen_affectation(instruction)
    elif type(instruction) == arbre_abstrait.Declaration:  
        gen_declaration(instruction)
    elif type(instruction) == arbre_abstrait.DeclarationAffectation:
        gen_declarationAffectation(instruction)
    elif type(instruction) == arbre_abstrait.Retourner:
        gen_retourner(instruction)
    elif type(instruction) == arbre_abstrait.AppelFonctionInstruction:
        gen_appel_fonction_instruction(instruction)
    else:
        erreur("génération type instruction non implémenté "+str(type(instruction)))

def gen_retourner(retour):
    global table_symboles
    
    if not table_symboles.est_dans_fonction():
        erreur("Instruction 'retourner' en dehors d'une fonction")
    
    type_expr = gen_expression(retour.valeur)
    type_fonction = table_symboles.obtenir_type_fonction_courante()
    
    if type_expr != type_fonction:
        erreur(f"Type de retour incorrect: attendu {type_fonction}, obtenu {type_expr}")
    
    arm_instruction("pop", "{r2}", "", "", "valeur de retour")
    arm_instruction("pop", "{fp,pc}", "", "", "retour de fonction")

def gen_appel_fonction_instruction(appel):
    gen_appel_fonction(appel.nom, appel.arguments)
    arm_instruction("pop", "{r0}", "", "", "ignorer le résultat")

def gen_appel_fonction(nom, arguments):
    global table_symboles
    
    type_retour = table_symboles.verifier_appel_fonction(nom, arguments)
    
    # Empiler les arguments dans l'ordre inverse
    for arg in reversed(arguments):
        gen_expression(arg)
    
    arm_instruction("bl", f"_{nom}", "", "", f"appel fonction {nom}")
    
    if len(arguments) > 0:
        arm_instruction("add", "sp", "sp", f"#{len(arguments)*4}", "dépiler les arguments")
    
    arm_instruction("push", "{r2}", "", "", "empiler le résultat")
    return type_retour

def gen_declarationAffectation(decl):
    global table_symboles
    
    type_expr = gen_expression(decl.expression)
    if type_expr != decl.type_variable:
        erreur(f"Type incompatible: variable {decl.type_variable}, expression {type_expr}")
    
    table_symboles.ajouter_variable(decl.nom_variable, decl.type_variable)
    arm_instruction("pop", "{r0}", "", "", f"valeur pour variable {decl.nom_variable}")
    arm_instruction("push", "{r0}", "", "", f"stocker variable {decl.nom_variable}")

def gen_declaration(decl):
    global table_symboles
    
    table_symboles.ajouter_variable(decl.nom, decl.type_variable)
    
    if decl.type_variable == 'entier':
        arm_instruction("mov", "r0", "#0", "", "valeur par défaut entier")
    else:
        arm_instruction("mov", "r0", "#0", "", "valeur par défaut booleen")
    
    arm_instruction("push", "{r0}", "", "", f"réserver espace pour {decl.nom}")

def gen_affectation(affect):
    global table_symboles
    
    if not table_symboles.variable_existe(affect.ident):
        erreur(f"Variable '{affect.ident}' non définie")
    
    var_info = table_symboles.obtenir_variable(affect.ident)
    type_expr = gen_expression(affect.expr)
    
    if type_expr != var_info['type']:
        erreur(f"Type incompatible pour affectation: variable {var_info['type']}, expression {type_expr}")
    
    arm_instruction("pop", "{r0}", "", "", "valeur à affecter")
    arm_instruction("str", "r0", f"[fp, #{var_info['adresse']}]", "", f"affecter à {affect.ident}")

def gen_ecrire(ecrire):
    gen_expression(ecrire.exp)
    arm_instruction("pop", "{r1}", "", "", "")
    arm_instruction("ldr", "r0", "=.LC1", "", "")
    arm_instruction("bl", "printf", "", "", "")

def gen_tantque(tantque):
    etiq_debut = arm_nouvelle_etiquette()
    etiq_fin = arm_nouvelle_etiquette()
    
    printifm(etiq_debut + ":")
    
    type_cond = gen_expression(tantque.condition)
    if type_cond != "booleen":
        erreur("Condition de 'tantque' doit être booléenne")
    
    arm_instruction("pop", "{r1}", "", "", "dépile la condition")
    arm_instruction("cmp", "r1", "#0", "", "teste si condition == 0 (faux)")
    arm_instruction("beq", etiq_fin, "", "", "saut si condition fausse")
    
    # Entrer dans un nouveau bloc pour les variables locales
    table_symboles.entrer_bloc()
    gen_listeInstructions(tantque.bloc)
    table_symboles.sortir_bloc()
    
    arm_instruction("b", etiq_debut, "", "", "retour au début de la boucle")
    printifm(etiq_fin + ":")

def gen_si(si):
    etiq_fin = arm_nouvelle_etiquette()
    etiq_sinon = arm_nouvelle_etiquette()
    
    type_cond = gen_expression(si.condition)
    if type_cond != "booleen":
        erreur("Condition de 'si' doit être booléenne")
    
    arm_instruction("pop", "{r1}", "", "", "dépile la condition")
    arm_instruction("cmp", "r1", "#0", "", "teste si condition == 0 (faux)")
    arm_instruction("beq", etiq_sinon, "", "", "saut si condition fausse")
    
    # Entrer dans un nouveau bloc pour les variables locales
    table_symboles.entrer_bloc()
    gen_listeInstructions(si.corps_si)
    table_symboles.sortir_bloc()
    
    arm_instruction("b", etiq_fin, "", "", "saut vers la fin")
    
    printifm(etiq_sinon + ":")
    
    if si.corps_sinon_si:
        for elif_block in si.corps_sinon_si:
            gen_elif(elif_block, etiq_fin)
    
    if si.corps_sinon:
        table_symboles.entrer_bloc()
        gen_listeInstructions(si.corps_sinon.corps_else)
        table_symboles.sortir_bloc()
    
    printifm(etiq_fin + ":")

def gen_elif(elif_block, etiq_fin):
    etiq_next = arm_nouvelle_etiquette()
    
    type_cond = gen_expression(elif_block.condition)
    if type_cond != "booleen":
        erreur("Condition de 'sinon si' doit être booléenne")
    
    arm_instruction("pop", "{r1}", "", "", "dépile la condition")
    arm_instruction("cmp", "r1", "#0", "", "teste si condition == 0 (faux)")
    arm_instruction("beq", etiq_next, "", "", "saut si condition fausse")
    
    # Entrer dans un nouveau bloc pour les variables locales
    table_symboles.entrer_bloc()
    gen_listeInstructions(elif_block.corps_elif)
    table_symboles.sortir_bloc()
    
    arm_instruction("b", etiq_fin, "", "", "saut vers la fin")
    printifm(etiq_next + ":")

def gen_lire(lire):
    arm_instruction("ldr", "r0", "=.LC0", "", "adresse du format %d")
    arm_instruction("sub", "sp", "sp", "#4", "réserver 4 octets sur la pile")
    arm_instruction("mov", "r1", "sp", "", "adresse où stocker l'entier lu")
    arm_instruction("bl", "scanf", "", "", "appel à scanf")
    arm_instruction("ldr", "r0", "[sp]", "", "charger l'entier lu")
    arm_instruction("add", "sp", "sp", "#4", "libérer la pile")
    arm_instruction("push", "{r0}", "", "", "empiler la valeur lue")

def gen_expression(expression):
    if type(expression) == arbre_abstrait.Operation:
        return gen_operation(expression) 
    elif type(expression) == arbre_abstrait.Entier:
        arm_instruction("mov", "r1", "#"+str(expression.valeur), "", "") 
        arm_instruction("push", "{r1}", "", "", "")
        return "entier"
    elif type(expression) == arbre_abstrait.Booleen:
        valeur = 1 if expression.valeur else 0
        arm_instruction("mov", "r1", "#"+str(valeur), "", "")
        arm_instruction("push", "{r1}", "", "", "")
        return "booleen"
    elif type(expression) == arbre_abstrait.Lire:
        gen_lire(expression)
        return "entier"
    elif type(expression) == arbre_abstrait.Variable:
        return gen_variable(expression)
    elif type(expression) == arbre_abstrait.AppelFonction:
        return gen_appel_fonction(expression.nom, expression.args)
    else:
        erreur("type d'expression inconnu "+str(type(expression)))

def gen_variable(variable):
    global table_symboles
    
    if not table_symboles.variable_existe(variable.nom):
        erreur(f"Variable '{variable.nom}' non définie")
    
    var_info = table_symboles.obtenir_variable(variable.nom)
    arm_instruction("ldr", "r2", f"[fp, #{var_info['adresse']}]", "", f"charger variable {variable.nom}")
    arm_instruction("push", "{r2}", "", "", "")
    
    return var_info['type']

def gen_operation(operation):
    op = operation.op

    if op == 'non':
        type1 = gen_expression(operation.exp1)
        if type1 != "booleen":
            erreur(f"Erreur de type : opérateur logique 'non' appliqué à un non-booléen")
        arm_instruction("pop", "{r0}", "", "", "dépile exp1 dans r0")
        arm_instruction("cmp", "r0", "#0", "", "compare à 0")
        arm_instruction("moveq", "r0", "#1", "", "si égal à 0 -> 1")
        arm_instruction("movne", "r0", "#0", "", "sinon -> 0")
        arm_instruction("push", "{r0}", "", "", "empile le résultat")
        operation.type = "booleen"
        return "booleen"

    type1 = gen_expression(operation.exp1)
    type2 = gen_expression(operation.exp2)

    arm_instruction("pop", "{r1}", "", "", "dépile exp2 dans r1")
    arm_instruction("pop", "{r0}", "", "", "dépile exp1 dans r0")

    if op in ['+', '-', '*', '/', '%']:
        if type1 != "entier" or type2 != "entier":
            erreur(f"Erreur de type : opérateur arithmétique '{op}' appliqué à des non-entiers")
        operation.type = "entier"
        
        if op == '+':
            arm_instruction("add", "r0", "r0", "r1", "effectue l'addition")
        elif op == '-':
            arm_instruction("sub", "r0", "r0", "r1", "effectue la soustraction")
        elif op == '*':
            arm_instruction("mov", "r2", "r0", "", "copie r0 dans r2")
            arm_instruction("mul", "r0", "r1", "r2", "r0 = r1 * r2")
        elif op == '/':
            arm_instruction("bl", "__aeabi_idiv", "", "", "division entière")
        elif op == '%':
            arm_instruction("bl", "__aeabi_idivmod", "", "", "modulo")
            arm_instruction("mov", "r0", "r1", "", "copie le reste")

    elif op in ['==', '!=', '<', '>', '<=', '>=']:
        if type1 != "entier" or type2 != "entier":
            erreur(f"Erreur de type : opérateur de comparaison '{op}' appliqué à des non-entiers")
        operation.type = "booleen"
        
        arm_instruction("cmp", "r0", "r1", "", "compare r0 et r1")
        etiq_vrai = arm_nouvelle_etiquette()
        etiq_fin = arm_nouvelle_etiquette()
        saut = {
            "==": "beq", "!=": "bne", "<": "blt",
            ">": "bgt", "<=": "ble", ">=": "bge"
        }
        arm_instruction(saut[op], etiq_vrai, "", "", f"saut si {op} est vrai")
        arm_instruction("mov", "r0", "#0", "", "résultat faux")
        arm_instruction("b", etiq_fin, "", "", "saut vers fin")
        printifm(etiq_vrai + ":")
        arm_instruction("mov", "r0", "#1", "", "résultat vrai")
        printifm(etiq_fin + ":")

    elif op in ['et', 'ou']:
        if type1 != "booleen" or type2 != "booleen":
            erreur(f"Erreur de type : opérateur logique '{op}' appliqué à des non-booléens")
        operation.type = "booleen"
        
        if op == 'et':
            arm_instruction("mul", "r0", "r0", "r1", "et booléen = multiplication")
        elif op == 'ou':
            arm_instruction("add", "r0", "r0", "r1", "ou logique: r0 + r1")
            arm_instruction("cmp", "r0", "#2", "", "compare avec 2")
            etiq_fin_ou = arm_nouvelle_etiquette()
            arm_instruction("blt", etiq_fin_ou, "", "", "saut si < 2")
            arm_instruction("mov", "r0", "#1", "", "si >= 2, mettre 1")
            printifm(etiq_fin_ou + ":")

    else:
        erreur("operateur \""+op+"\" non implémenté")

    arm_instruction("push",  "{r0}" , "", "", "empile le résultat")
    return operation.type


if __name__ == "__main__":
    lexer = FloLexer()
    parser = FloParser()
    
    if len(sys.argv) < 3 or sys.argv[1] not in ["-arm","-table"]:
        print("usage: python3 generation_code.py -arm|-table NOM_FICHIER_SOURCE.flo")
        exit(1)
        
    if sys.argv[1] == "-arm":
        afficher_code = True
    else:
        afficher_table = Truea
        
    # INITIALISATION OBLIGATOIRE
    table_symboles = TableDesSymboles()
    
    with open(sys.argv[2],"r") as f:
        data = f.read()
        try:
            arbre = parser.parse(lexer.tokenize(data))
            gen_programme(arbre)
        except EOFError:
            exit(1)