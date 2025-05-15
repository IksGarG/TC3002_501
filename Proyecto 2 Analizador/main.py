from globalTypes import * 
from parser import parse, recibeParser 
    

def main():
    fileName = "sample"
    with open(fileName + ".c-", "r") as f:
        program = f.read()
    progLong = len(program)
    program_with_eof = program + "$"
    startPos   = 0
    recibeParser(program_with_eof, startPos, progLong)
    
    syntaxTree = parse(True)
    if syntaxTree is None:
        print("Error: El árbol de sintaxis es nulo.")
        return

if __name__ == "__main__":
    main()