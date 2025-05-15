# semantica.py
from globalTypes import *
from symtab import *

Error = False
skip_simple_params = set()

# Stack for tracking current function return types (if needed)
current_func_returns = []

def tipo_error(t, message, expected_type=None):
    """
    Imprime el mensaje con línea y token, marca Error y
    para recuperación asigna el tipo esperado (si se indica).
    """
    global Error
    print(f"Línea {t.lineno}: {message}")
    Error = True
    if expected_type is not None:
        t.type = expected_type


def traverse(t, pre, post):
    if t is None:
        return
    pre(t)
    for c in t.child:
        traverse(c, pre, post)
    post(t)
    traverse(t.sibling, pre, post)


def insertar_nodo(t):
    """
    Inserta nodos en la tabla de símbolos.
    Se ejecuta en preorder.
    """
    global skip_simple_params

    # Rechazar variables de tipo void
    if t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.DeclK and t.child[1] is None and t.type == ExpType.Void:
        tipo_error(t, "Declaración de variable con tipo void no permitida")
        return

    # --- Función: DeclK con cuerpo en child[1] ---
    if t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.DeclK and t.child[1] is not None:
        # Registrar firma de función
        param_names = []
        p = t.child[0]
        while p and p.nodekind == NodeKind.StmtK and p.stmt == StmtKind.DeclK:
            param_names.append(p.name)
            p = p.sibling
        # Tipo de parámetros
        param_list = []
        p = t.child[0]
        while p and p.name in param_names:
            param_list.append(p.type)
            p = p.sibling
        st_insert_func(t.name, t.lineno, t.type, param_list)
        # Nuevo scope
        st_enter_scope()
        # Insertar parámetros
        for pname in param_names:
            st_insert(pname, t.lineno)
        skip_simple_params.update(param_names)
        # TODO: Soporte completo de arreglos (var ID[NUM] y parámetros ID[])
        return

    # --- Nuevo bloque compuesto { ... } ---
    if t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.CompoundK:
        st_enter_scope()
        return

    # --- Declaraciones de variable sencillas ---
    if t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.DeclK:
        if t.name in skip_simple_params:
            skip_simple_params.remove(t.name)
            return
        if not st_insert(t.name, t.lineno):
            tipo_error(t, f"'{t.name}' ya definido en este scope")
        return

    # --- Uso de identificador ---
    if t.nodekind == NodeKind.ExpK and t.exp == ExpKind.IdK:
        entry = st_lookup(t.name)
        if entry is None:
            tipo_error(t, f"Uso de variable no declarada '{t.name}'", ExpType.Integer)
        else:
            if t.lineno not in entry.use_lines:
                entry.use_lines.append(t.lineno)


def salir_nodo(t):
    """
    Cierra scopes abiertos en insertar_nodo.
    """
    # Salir de función
    if t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.DeclK and t.child[1] is not None:
        current_func_returns.pop() if current_func_returns else None
        st_exit_scope()
    # Salir de bloque
    elif t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.CompoundK:
        st_exit_scope()


def check_node(t):
    """
    Comprueba tipos en postorder.
    """
    # ----- Operaciones y comparaciones -----
    if t.nodekind == NodeKind.ExpK and t.exp == ExpKind.OpK:
        l, r = t.child[0], t.child[1]
        if l.type != ExpType.Integer or r.type != ExpType.Integer:
            tipo_error(t, "Operador aplicado a no enteros", ExpType.Integer)
        # Comparaciones también resultan en Integer (0 o 1)
        t.type = ExpType.Integer

    # ----- Constantes e ids -----
    elif t.nodekind == NodeKind.ExpK and t.exp in (ExpKind.ConstK, ExpKind.IdK):
        t.type = ExpType.Integer

    # ----- Llamadas a función -----
    elif t.nodekind == NodeKind.ExpK and t.exp == ExpKind.CallK:
        entry = st_lookup(t.name)
        if entry is None or not entry.is_func:
            tipo_error(t, f"Llamada a función no declarada '{t.name}'", ExpType.Integer)
        else:
            # Extraer args via sibling chain
            args = []
            p = t.child[0]
            while p:
                args.append(p)
                p = p.sibling
            if len(args) != len(entry.param_types):
                tipo_error(t,
                           f"'{t.name}' espera {len(entry.param_types)} args, got {len(args)}",
                           entry.return_type)
            else:
                for idx, (ai, expected) in enumerate(zip(args, entry.param_types), start=1):
                    if ai.type != expected:
                        tipo_error(ai,
                                   f"Arg {idx} de '{t.name}' debe ser {expected}",
                                   expected)
            t.type = entry.return_type

    # ----- Sentencias -----
    elif t.nodekind == NodeKind.StmtK:
        # If y While requieren Integer (0=false, !=0 true)
        if t.stmt == StmtKind.IfK or t.stmt == StmtKind.WhileK:
            test = t.child[0]
            if test is None or test.type != ExpType.Integer:
                tipo_error(test or t, f"Condición de {t.stmt.name.lower()} no es Integer", ExpType.Integer)
        elif t.stmt == StmtKind.AssignK:
            # Asegurar que el LHS sea variable (o acceso a arreglo)
            # Verificar que existan ambos operandos
            if t.child[0] is None or t.child[1] is None:
                tipo_error(t, "Asignación con operando faltante", ExpType.Integer)
                return
            lhs = t.child[0]
            if not (lhs.nodekind == NodeKind.ExpK and lhs.exp == ExpKind.IdK):
                tipo_error(lhs, "Lado izquierdo de asignación debe ser variable o acceso a arreglo", ExpType.Integer)
            lhs, rhs = t.child[0], t.child[1]
            if lhs.type != ExpType.Integer or rhs.type != ExpType.Integer:
                tipo_error(t, "Asignación con tipos no enteros", ExpType.Integer)
        elif t.stmt == StmtKind.OutputK:
            if t.child[0] is None or t.child[0].type != ExpType.Integer:
                tipo_error(t, "Output de no entero", ExpType.Integer)
        elif t.stmt == StmtKind.InputK:
            if t.child[0] is None or t.child[0].type != ExpType.Integer:
                tipo_error(t, "Input de no entero", ExpType.Integer)
        elif t.stmt == StmtKind.ReturnK:
                pass


def tabla(tree, imprime=True):
    """
    Construye la tabla de símbolos (sin poppear scopes)
    e imprime todos los scopes acumulados.
    """
    st_reset()
    st_enter_scope()      # scope global
    init_builtins()       # input/output

    # Sólo preorder: insertar_nodo, sin postProc
    traverse(tree, insertar_nodo, lambda t: None)

    if imprime:
        print("=== Tablas de símbolos ===")
        printSymTab()


def semantica(tree, imprime=True):
    """Driver semántico: tabla + chequeo de tipos con recuperación."""
    tabla(tree, imprime)
    # Verificar que la última declaración sea main() de tipo void
    last_decl = tree
    while last_decl and last_decl.sibling:
        last_decl = last_decl.sibling
    if not (last_decl.nodekind == NodeKind.StmtK
            and last_decl.stmt == StmtKind.DeclK
            and last_decl.name == "main"
            and last_decl.child[1] is not None
            and last_decl.type == ExpType.Void):
        tipo_error(last_decl, "Última declaración debe ser función 'main' de tipo void")
    traverse(tree, lambda t: None, check_node)
    if not Error:
        print("¡Sin errores semánticos detectados!")
