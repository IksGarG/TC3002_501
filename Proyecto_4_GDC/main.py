import sys

def main():
    from parser import recibeParser, parse
    from semantica import semantica
    from symtab import init_builtins, st_reset, st_enter_scope
    from cgen import codeGen

    f = open(sys.argv[1], 'r')
    prog = f.read()
    f.close()

    # Inicializar parser y symtab
    recibeParser(prog, 0, len(prog))
    st_reset()
    st_enter_scope()
    init_builtins()

    AST = parse(True)
    semantica(AST, True)
    codeGen(AST, sys.argv[2] if len(sys.argv) > 2 else 'out.s')

if __name__ == '__main__':
    main()