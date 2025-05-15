from globalTypes import *
from parser import parse, recibeParser
from semantica import semantica

f = open('sample.c-', 'r')
programa = f.read()
progLong = len(programa)
programa += '$'
posicion = 0

# Inicializar globals en parser
recibeParser(programa, posicion, progLong)
AST = parse(True)

# Ejecutar semántica
semantica(AST, True)