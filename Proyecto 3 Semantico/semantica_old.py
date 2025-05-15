# semantica.py
from globalTypes import *
from symtab import *

Error = False
skip_simple_params = set()

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
    Se ejecuta en preorder, y se encarga de abrir y cerrar
    scopes según el tipo de nodo. \n
    Esta función empezo con un fallo de manejo de los nodos y se corrigio con una IA
    """
    global skip_simple_params
    #Debug print
    # print(f"[DBG] insertar_nodo: stmt={t.stmt}, name={t.name}, lineno={t.lineno}")

    # --- Función: DeclK con body en child[1] ---
    if t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.DeclK and t.child[1] is not None:
        # 1) Recoger nombres de parámetros (hijos DeclK antes del CompoundK)
        param_names = []
        p = t.child[0]
        while p is not None and p.nodekind == NodeKind.StmtK and p.stmt == StmtKind.DeclK:
            param_names.append(p.name)
            p = p.sibling
        # 2) Param types extraídos de cada DeclK.param.type
        param_list = []
        p = t.child[0]
        while p is not None and p.name in param_names:
            param_list.append(p.type)
            p = p.sibling

        # 3) Registrar función en tabla global
        st_insert_func(t.name, t.lineno, t.type, param_list)

        # 4) Entrar en nuevo scope y registrar parámetros como variables locales
        st_enter_scope()
        for pname in param_names:
            st_insert(pname, t.lineno)

        # 5) Guardar nombres para saltarlos en la rama simple
        skip_simple_params.update(param_names)
        return

    # --- Nuevo bloque compuesto { ... } ---
    if t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.CompoundK:
        st_enter_scope()
        return

    # --- Declaraciones de variable sencillas ---
    if t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.DeclK:
        # si es un parámetro recién insertado, lo saltamos
        if t.name in skip_simple_params:
            skip_simple_params.remove(t.name)
            return
        # insertar variable normal
        if not st_insert(t.name, t.lineno):
            tipo_error(t, f"'{t.name}' ya definido en este scope")
        return

    # --- Uso de identificador (ExpKind.IdK) ---
    if t.nodekind == NodeKind.ExpK and t.exp == ExpKind.IdK:
        entry = st_lookup(t.name)
        if entry is None:
            tipo_error(t, f"Uso de variable no declarada '{t.name}'", ExpType.Integer)
        else:
            if t.lineno not in entry.use_lines:
                entry.use_lines.append(t.lineno)
    
    # Nuevo bloque compuesto
    if t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.CompoundK:
        st_enter_scope()
        return
    
     # Declaraciones de variable simples (esto ya no afectará a los parámetros)
    if t.nodekind == NodeKind.StmtK and t.stmt == StmtKind.DeclK:
        if not st_insert(t.name, t.lineno):
            tipo_error(t, f"'{t.name}' ya definido en este scope")
        return

    # --- Uso de identificador (expresión IdK) ---
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
    if t.nodekind == NodeKind.StmtK and ((t.stmt == StmtKind.DeclK and t.child[1] is not None) or t.stmt == StmtKind.CompoundK):
        st_exit_scope()

def check_node(t):
    # print(f"[DBG] check_node: stmt={t.stmt}, exp={t.exp}, line={t.lineno}")
    """
    Comprueba tipos en postorder.
    """
    # ----- Operaciones binarias -----
    if t.nodekind == NodeKind.ExpK and t.exp == ExpKind.OpK:
        l, r = t.child[0], t.child[1]
        if l.type != ExpType.Integer or r.type != ExpType.Integer:
            tipo_error(t, "Operador aplicado a no enteros", ExpType.Integer)
        # comparadores devuelven Boolean, resto Integer
        if t.op in (TokenType.LT, TokenType.EQ):
            t.type = ExpType.Boolean
        else:
            t.type = ExpType.Integer

    # ----- Constantes e ids -----
    elif t.nodekind == NodeKind.ExpK and t.exp in (ExpKind.ConstK, ExpKind.IdK):
        t.type = ExpType.Integer

    elif t.nodekind == NodeKind.ExpK and t.exp == ExpKind.CallK:
        entry = st_lookup(t.name)
        if entry is None or not entry.is_func:
            tipo_error(t, f"Llamada a función no declarada '{t.name}'", ExpType.Integer)
        else:
            # 1) Cada hijo no-None es un argumento directo
            args = []
            p = t.child[0]
            while p is not None:
                args.append(p)
                p = p.sibling
            # print(f"[DBG] CALL {t.name}: extraídos {len(args)} args (espera {len(entry.param_types)})")
            # 2) Conteo y chequeo
            if len(args) != len(entry.param_types):
                tipo_error(
                    t,
                    f"'{t.name}' espera {len(entry.param_types)} args, got {len(args)}",
                    entry.return_type
                )
            else:
                for idx, (ai, expected) in enumerate(zip(args, entry.param_types), start=1):
                    if ai.type != expected:
                        tipo_error(
                            ai,
                            f"Arg {idx} de '{t.name}' debe ser {expected}",
                            expected
                        )
            # 3) Propagamos el tipo de retorno
            t.type = entry.return_type

    # ----- Sentencias -----
    elif t.nodekind == NodeKind.StmtK:
        if t.stmt == StmtKind.IfK:
            test = t.child[0]
            if test.type != ExpType.Boolean:
                tipo_error(test, "Condición de if no booleana", ExpType.Boolean)
        elif t.stmt == StmtKind.WhileK:
            test = t.child[0]
            if test.type != ExpType.Boolean:
                tipo_error(test, "Condición de while no booleana", ExpType.Boolean)
        elif t.stmt == StmtKind.AssignK:
            lhs, rhs = t.child[0], t.child[1]
            if lhs.type != ExpType.Integer or rhs.type != ExpType.Integer:
                tipo_error(t, "Asignación con tipos no enteros", ExpType.Integer)
        elif t.stmt == StmtKind.OutputK:
            if t.child[0].type != ExpType.Integer:
                tipo_error(t, "Output de no entero", ExpType.Integer)
        elif t.stmt == StmtKind.InputK:
            if t.child[0].type != ExpType.Integer:
                tipo_error(t, "Input de no entero", ExpType.Integer)
        elif t.stmt == StmtKind.ReturnK:
            # comprobar tipo de retorno contra función actual
            # puedes guardar en un global la firma actual
            pass  # implementar según tu AST

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
    traverse(tree, lambda t: None, check_node)
    if not Error:
        print("¡Sin errores semánticos detectados!")