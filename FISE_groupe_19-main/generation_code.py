# generation_code.py

import sys
from analyse_lexicale import FloLexer
from analyse_syntaxique import FloParser
import arbre_abstrait
from table_des_symboles import TableDesSymboles

num_etiquette_courante = -1
afficher_table = False
afficher_code = False
table_symboles = None
function_end_labels = []

def erreur(s):
    print("Erreur:", s, file=sys.stderr)
    exit(1)

def printifm(*args, **kwargs):
    if afficher_code:
        print(*args, **kwargs)

def printift(*args, **kwargs):
    if afficher_table:
        print(*args, **kwargs)

def arm_comment(comment):
    if comment:
        printifm("\t\t @ " + comment)
    else:
        printifm("")

def arm_instruction(opcode, op1="", op2="", op3="", comment=""):
    if op2 == "":
        printifm(f"\t{opcode}\t{op1}\t\t", end="")
    elif op3 == "":
        printifm(f"\t{opcode}\t{op1},\t{op2}\t", end="")
    else:
        printifm(f"\t{opcode}\t{op1},\t{op2},\t{op3}", end="")
    arm_comment(comment)

def arm_nouvelle_etiquette():
    global num_etiquette_courante
    num_etiquette_courante += 1
    return f"e{num_etiquette_courante}"

def gather_locals_in_list(instr_list):
    locals_list = []
    from arbre_abstrait import Declaration, DeclarationAffectation, Tantque, Si
    for instr in instr_list.instructions:
        if isinstance(instr, Declaration):
            locals_list.append((instr.nom, instr.type_variable))
        elif isinstance(instr, DeclarationAffectation):
            locals_list.append((instr.nom_variable, instr.type_variable))
        if isinstance(instr, Tantque):
            locals_list += gather_locals_in_list(instr.bloc)
        elif isinstance(instr, Si):
            locals_list += gather_locals_in_list(instr.corps_si)
            for e in instr.corps_sinon_si or []:
                locals_list += gather_locals_in_list(e.corps_elif)
            if instr.corps_sinon:
                locals_list += gather_locals_in_list(instr.corps_sinon.corps_else)
    return locals_list

def gen_programme(programme):
    global table_symboles
    table_symboles = TableDesSymboles()
    header = """.LC0:
    .ascii "%d\\000"
    .align 2
.LC1:
    .ascii "%d\\012\\000"
    .text
    .align 2
    .global main
    .global __aeabi_idiv
    .global __aeabi_idivmod"""
    printifm(header)
    for fonction in programme.listeFonctions.fonctions:
        params = [(p.type_param, p.nom) for p in fonction.parametres.parametres]
        table_symboles.ajouter_fonction(fonction.nom, fonction.type_retour, params)
    if afficher_table:
        table_symboles.afficher()
        return
    for fonction in programme.listeFonctions.fonctions:
        gen_fonction(fonction)
    table_symboles.ajouter_fonction("main", "entier", [])
    printifm("main:")
    table_symboles.entrer_contexte_fonction("main")
    local_list = gather_locals_in_list(programme.listeInstructions)
    param_count = 0
    local_count = len(local_list)
    locals_size = 4 * (param_count + local_count)
    if locals_size % 8 != 0:
        locals_size += 4
    arm_instruction("push", "{fp,lr}", "", "", "")
    arm_instruction("mov", "fp", "sp", "", "")
    if locals_size > 0:
        arm_instruction("sub", "sp", "sp", f"#{locals_size}", "")
    for idx, (nom, typ) in enumerate(local_list):
        offset = -4 * (idx + 1)
        table_symboles.ajouter_variable(nom, typ, offset)
        arm_instruction("mov", "r0", "#0", "", "")
        arm_instruction("str", "r0", f"[fp,#{offset}]", "", "")
    gen_listeInstructions(programme.listeInstructions)
    arm_instruction("mov", "r0", "#0", "", "")
    if locals_size > 0:
        arm_instruction("add", "sp", "sp", f"#{locals_size}", "")
    arm_instruction("pop", "{fp, pc}", "", "", "")
    table_symboles.sortir_contexte_fonction()

def gen_fonction(fonction):
    global table_symboles
    table_symboles.entrer_contexte_fonction(fonction.nom)
    local_list = gather_locals_in_list(fonction.corps)
    param_count = len(fonction.parametres.parametres)
    local_count = len(local_list)
    total_vars = param_count + local_count
    locals_size = 4 * total_vars
    if locals_size % 8 != 0:
        locals_size += 4
    printifm(f"_{fonction.nom}:")
    arm_instruction("push", "{fp,lr}", "", "", "")
    arm_instruction("mov", "fp", "sp", "", "")
    arm_instruction("sub", "sp", "sp", f"#{locals_size}", "",)
    end_label = f"{fonction.nom}_end"
    function_end_labels.append(end_label)
    for i, param in enumerate(fonction.parametres.parametres):
        if i < 4:
            offset = -4 * (i + 1)
            table_symboles.ajouter_variable(param.nom, param.type_param, offset)
            arm_instruction("str", f"r{i}", f"[fp,#{offset}]", "", "")
        else:
            erreur(f"Fonction {fonction.nom}: plus de 4 paramètres non supportés")
    for idx, (nom, typ) in enumerate(local_list):
        offset = -4 * (param_count + idx + 1)
        table_symboles.ajouter_variable(nom, typ, offset)
        arm_instruction("mov", "r0", "#0", "", "")
        arm_instruction("str", "r0", f"[fp,#{offset}]", "", "")
    gen_listeInstructions(fonction.corps)
    # suppression de "mov r2, #0" : on n'utilise plus r2 pour le retour
    arm_instruction("b", end_label, "", "", "")
    printifm(f"{end_label}:")
    arm_instruction("add", "sp", "sp", f"#{locals_size}", "",)
    arm_instruction("pop", "{fp,pc}", "", "", "")
    function_end_labels.pop()
    table_symboles.sortir_contexte_fonction()

def gen_listeInstructions(listeInstructions):
    for instr in listeInstructions.instructions:
        gen_instruction(instr)

def gen_instruction(instr):
    if isinstance(instr, arbre_abstrait.Ecrire):
        gen_ecrire(instr)
    elif isinstance(instr, arbre_abstrait.Tantque):
        gen_tantque(instr)
    elif isinstance(instr, arbre_abstrait.Si):
        gen_si(instr)
    elif isinstance(instr, arbre_abstrait.Affectation):
        gen_affectation(instr)
    elif isinstance(instr, arbre_abstrait.Declaration):
        gen_declaration(instr)
    elif isinstance(instr, arbre_abstrait.DeclarationAffectation):
        gen_declarationAffectation(instr)
    elif isinstance(instr, arbre_abstrait.Retourner):
        gen_retourner(instr)
    elif isinstance(instr, arbre_abstrait.AppelFonctionInstruction):
        gen_appel_fonction_instruction(instr)
    else:
        erreur("Type instruction non implémenté: " + str(type(instr)))

def gen_retourner(retour):
    global table_symboles
    if not table_symboles.est_dans_fonction():
        erreur("`retourner` en dehors d'une fonction")
    typ = gen_expression(retour.valeur)
    if typ != table_symboles.obtenir_type_fonction_courante():
        erreur("Type de retour incorrect")
    arm_instruction("pop", "{r0}", "", "", "")  # valeur de retour en r0
    if not function_end_labels:
        erreur("Pas de label de fin pour la fonction lors de 'retourner'")
    end_label = function_end_labels[-1]
    arm_instruction("b", end_label, "", "", "")

def gen_appel_fonction_instruction(appel):
    gen_appel_fonction(appel.nom, appel.arguments)
    arm_instruction("pop", "{r0}", "", "", "")  # consommer le résultat si non utilisé

def gen_appel_fonction(nom, args):
    global table_symboles
    typ = table_symboles.verifier_appel_fonction(nom, args)
    n = len(args)
    # 1) Empiler toutes les valeurs d'arguments
    for a in args:
        if isinstance(a, arbre_abstrait.Entier):
            arm_instruction("mov", "r1", f"#{a.valeur}", "", "chargement littéral")
            arm_instruction("push", "{r1}", "", "", "")
        elif isinstance(a, arbre_abstrait.Booleen):
            v = 1 if a.valeur else 0
            arm_instruction("mov", "r1", f"#{v}", "", "chargement booléen")
            arm_instruction("push", "{r1}", "", "", "")
        else:
            gen_expression(a)
    # 2) Pop en ordre inverse dans r0..r{n-1}
    for i in reversed(range(n)):
        arm_instruction("pop", "{r" + str(i) + "}", "", "", f"charger argument {i}")
    # 3) Appel
    arm_instruction("bl", f"_{nom}", "", "", f"appel {nom}")
    # 4) Empiler le résultat si on veut conserver sur la pile
    arm_instruction("push", "{r0}", "", "", "empiler résultat")
    return typ


def gen_declarationAffectation(decl):
    t = gen_expression(decl.expression)
    if t != decl.type_variable:
        erreur("Type incompatible en déclaration-affectation")
    arm_instruction("pop", "{r0}", "", "", "")
    info = table_symboles.obtenir_variable(decl.nom_variable)
    arm_instruction("str", "r0", f"[fp,#{info['adresse']}]", "", "")

def gen_declaration(decl):
    info = table_symboles.obtenir_variable(decl.nom)
    arm_instruction("mov", "r0", "#0", "", "")
    arm_instruction("str", "r0", f"[fp,#{info['adresse']}]", "", "")

def gen_affectation(affect):
    if not table_symboles.variable_existe(affect.ident):
        erreur("Variable non définie")
    var = table_symboles.obtenir_variable(affect.ident)
    t = gen_expression(affect.expr)
    if t != var['type']:
        erreur("Type incompatible en affectation")
    arm_instruction("pop", "{r0}", "", "", "")
    arm_instruction("str", "r0", f"[fp,#{var['adresse']}]", "", "")

def gen_ecrire(ecrire):
    gen_expression(ecrire.exp)
    arm_instruction("pop", "{r1}", "", "", "")
    arm_instruction("ldr", "r0", "=.LC1", "", "")
    arm_instruction("bl", "printf", "", "", "")

def gen_tantque(tantque):
    d = arm_nouvelle_etiquette()
    f = arm_nouvelle_etiquette()
    printifm(f"{d}:")
    if gen_expression(tantque.condition) != "booleen":
        erreur("Condition de 'tantque' doit être booléenne")
    arm_instruction("pop", "{r1}", "", "", "")
    arm_instruction("cmp", "r1", "#0", "", "")
    arm_instruction("beq", f, "", "", "")
    table_symboles.entrer_bloc()
    gen_listeInstructions(tantque.bloc)
    table_symboles.sortir_bloc()
    arm_instruction("b", d, "", "", "")
    printifm(f"{f}:")

def gen_si(si):
    fin = arm_nouvelle_etiquette()
    sinon = arm_nouvelle_etiquette()
    if gen_expression(si.condition) != "booleen":
        erreur("Condition de 'si' doit être booléenne")
    arm_instruction("pop", "{r1}", "", "", "")
    arm_instruction("cmp", "r1", "#0", "", "")
    arm_instruction("beq", sinon, "", "", "")
    table_symboles.entrer_contexte_fonction  # pas modifié
    table_symboles.entrer_bloc()
    gen_listeInstructions(si.corps_si)
    table_symboles.sortir_bloc()
    arm_instruction("b", fin, "", "", "")
    printifm(f"{sinon}:")
    for e in si.corps_sinon_si or []:
        gen_elif(e, fin)
    if si.corps_sinon:
        table_symboles.entrer_bloc()
        gen_listeInstructions(si.corps_sinon.corps_else)
        table_symboles.sortir_bloc()
    printifm(f"{fin}:")

def gen_elif(elif_b, fin):
    nxt = arm_nouvelle_etiquette()
    if gen_expression(elif_b.condition) != "booleen":
        erreur("Condition de 'sinon si' doit être booléenne")
    arm_instruction("pop", "{r1}", "", "", "")
    arm_instruction("cmp", "r1", "#0", "", "")
    arm_instruction("beq", nxt, "", "", "")
    table_symboles.entrer_bloc()
    gen_listeInstructions(elif_b.corps_elif)
    table_symboles.sortir_bloc()
    arm_instruction("b", fin, "", "", "")
    printifm(f"{nxt}:")

def gen_lire(lire):
    arm_instruction("sub", "sp", "sp", "#8", "",)
    arm_instruction("mov", "r1", "sp", "", "")
    arm_instruction("ldr", "r0", "=.LC0", "", "")
    arm_instruction("bl", "scanf", "", "", "")
    arm_instruction("ldr", "r0", "[sp]", "", "")
    arm_instruction("add", "sp", "sp", "#8", "",)
    arm_instruction("push", "{r0}", "", "", "")

def gen_expression(expr):
    if isinstance(expr, arbre_abstrait.Operation):
        return gen_operation(expr)
    if isinstance(expr, arbre_abstrait.Entier):
        arm_instruction("mov", "r1", "#" + str(expr.valeur), "", "")
        arm_instruction("push", "{r1}", "", "", "")
        return "entier"
    if isinstance(expr, arbre_abstrait.Booleen):
        v = 1 if expr.valeur else 0
        arm_instruction("mov", "r1", "#" + str(v), "", "")
        arm_instruction("push", "{r1}", "", "", "")
        return "booleen"
    if isinstance(expr, arbre_abstrait.Lire):
        gen_lire(expr)
        return "entier"
    if isinstance(expr, arbre_abstrait.Variable):
        return gen_variable(expr)
    if isinstance(expr, arbre_abstrait.AppelFonction):
        return gen_appel_fonction(expr.nom, expr.args)
    erreur("Expression inconnue: " + str(type(expr)))

def gen_variable(var):
    if not table_symboles.variable_existe(var.nom):
        erreur("Variable non définie: " + var.nom)
    info = table_symboles.obtenir_variable(var.nom)
    arm_instruction("ldr", "r2", f"[fp,#{info['adresse']}]", "", "")
    arm_instruction("push", "{r2}", "", "", "")
    return info['type']

def gen_operation(opn):
    if opn.op == 'non':
        if gen_expression(opn.exp1) != "booleen":
            erreur("'non' appliqué à non-booléen")
        arm_instruction("pop", "{r0}", "", "", "")
        arm_instruction("cmp", "r0", "#0", "", "")
        arm_instruction("moveq", "r0", "#1", "", "")
        arm_instruction("movne", "r0", "#0", "", "")
        arm_instruction("push", "{r0}", "", "", "")
        return "booleen"
    t1 = gen_expression(opn.exp1)
    t2 = gen_expression(opn.exp2)
    arm_instruction("pop", "{r1}", "", "", "")
    arm_instruction("pop", "{r0}", "", "", "")
    if opn.op in ['+', '-', '*', '/', '%']:
        if t1 != "entier" or t2 != "entier":
            erreur("Op arithmétique sur non-entiers")
        if opn.op == '+':
            arm_instruction("add", "r0", "r0", "r1", "")
        elif opn.op == '-':
            arm_instruction("sub", "r0", "r0", "r1", "")
        elif opn.op == '*':
            arm_instruction("mul", "r2", "r1", "r0", "")
            arm_instruction("mov", "r0", "r2", "", "")
        elif opn.op == '/':
            arm_instruction("bl", "__aeabi_idiv", "", "", "")
        elif opn.op == '%':
            arm_instruction("bl", "__aeabi_idivmod", "", "", "")
            arm_instruction("mov", "r0", "r1", "", "")
        opn.type = "entier"
    elif opn.op in ['==','!=','<','>','<=','>=']:
        if t1 != "entier" or t2 != "entier":
            erreur("Comparaison sur non-entiers")
        arm_instruction("cmp", "r0", "r1", "", "")
        vrai = arm_nouvelle_etiquette()
        fin  = arm_nouvelle_etiquette()
        saut = {"==":"beq","!=":"bne","<":"blt",">":"bgt","<=":"ble",">=":"bge"}[opn.op]
        arm_instruction(saut, vrai, "", "", "")
        arm_instruction("mov", "r0", "#0", "", "")
        arm_instruction("b", fin, "", "", "")
        printifm(f"{vrai}:")
        arm_instruction("mov", "r0", "#1", "", "")
        printifm(f"{fin}:")
        opn.type = "booleen"
    elif opn.op in ['et','ou']:
        if t1 != "booleen" or t2 != "booleen":
            erreur("Logique sur non-booléens")
        if opn.op == 'et':
            arm_instruction("mul", "r2", "r0", "r1", "")
            arm_instruction("mov", "r0", "r2", "", "")
        else:
            arm_instruction("add", "r0", "r0", "r1", "")
            arm_instruction("cmp", "r0", "#2", "", "")
            next_ = arm_nouvelle_etiquette()
            arm_instruction("blt", next_, "", "", "")
            arm_instruction("mov", "r0", "#1", "", "")
            printifm(f"{next_}:")
        opn.type = "booleen"
    else:
        erreur("Opérateur non implémenté: " + opn.op)
    arm_instruction("push", "{r0}", "", "", "")
    return opn.type

if __name__ == "__main__":
    lexer = FloLexer()
    parser = FloParser()
    if len(sys.argv) < 3 or sys.argv[1] not in ["-arm", "-table"]:
        print("usage: python3 generation_code.py -arm|-table SOURCE.flo")
        exit(1)
    if sys.argv[1] == "-arm":
        afficher_code = True
    else:
        afficher_table = True
    with open(sys.argv[2], "r") as f:
        data = f.read()
        try:
            arbre = parser.parse(lexer.tokenize(data))
            gen_programme(arbre)
        except EOFError:
            exit(1)
