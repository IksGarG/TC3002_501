## Proyecto 4 Generador de Código
### Creado por Fernanda Cantú Ortega e Iker Garcia German.

Este proyecto es un generador de código MIPS para el lenguaje C-. Dado un AST (Árbol de Sintaxis Abstracta) de un programa en C-, produce el ensamblador MIPS equivalente, gestionando segmentos de datos, funciones, variables y estructuras de control.

#### Uso

1. Generar el código ensamblador:
   ```bash
   python main.py <input_ast_file> <output_asm_file>
   ```

2. Cargar y ejecutar el ensamblador en SPIM:
   ```bash
   spim -file <output_asm_file>
   ```