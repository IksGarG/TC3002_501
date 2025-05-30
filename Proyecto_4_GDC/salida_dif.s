.data

.text
.globl main
j main
# función gcd
gcd:
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
addi $fp, $sp, 8
addi $sp, $sp, -12
sw $a0, -12($fp)
sw $a1, -16($fp)
while_start_0:
lw $a0, -16($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0, 0
lw $t1, 0($sp)
addi $sp, $sp, 4
sne $a0, $t1, $a0
beqz $a0, while_end_1
lw $a0, -12($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, -12($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, -16($fp)
lw $t1, 0($sp)
addi $sp, $sp, 4
div $t1, $a0
mflo $a0
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, -16($fp)
lw $t1, 0($sp)
addi $sp, $sp, 4
mul $a0, $t1, $a0
lw $t1, 0($sp)
addi $sp, $sp, 4
subu $a0, $t1, $a0
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, 0($sp)
sw $a0, -20($fp)
addi $sp, $sp, 4
lw $a0, -16($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, 0($sp)
sw $a0, -12($fp)
addi $sp, $sp, 4
lw $a0, -20($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, 0($sp)
sw $a0, -16($fp)
addi $sp, $sp, 4
j while_start_0
while_end_1:
lw $a0, -12($fp)
move $v0, $a0
# return statement processed, $v0 holds return value if any. Control flows to epilogue.
move $sp, $fp
lw $ra, -8($fp)
lw $fp, -4($fp)
jr $ra
# función fib
fib:
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
addi $fp, $sp, 8
addi $sp, $sp, -4
sw $a0, -12($fp)
lw $a0, -12($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0, 0
lw $t1, 0($sp)
addi $sp, $sp, 4
seq $a0, $t1, $a0
beqz $a0, else_2
li $a0, 0
move $v0, $a0
# return statement processed, $v0 holds return value if any. Control flows to epilogue.
j endif_3
else_2:
lw $a0, -12($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0, 1
lw $t1, 0($sp)
addi $sp, $sp, 4
seq $a0, $t1, $a0
beqz $a0, else_4
li $a0, 1
move $v0, $a0
# return statement processed, $v0 holds return value if any. Control flows to epilogue.
j endif_5
else_4:
# Guardando $a0-$a3 del llamador antes de la llamada a fib
addi $sp, $sp, -16
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $a2, 8($sp)
sw $a3, 12($sp)
lw $a0, -12($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0, 1
lw $t1, 0($sp)
addi $sp, $sp, 4
subu $a0, $t1, $a0
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, 0($sp)
addi $sp, $sp, 4
jal fib
move $t0, $v0
# Restaurando $a0-$a3 del llamador después de la llamada a fib
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $a2, 8($sp)
lw $a3, 12($sp)
addi $sp, $sp, 16
move $a0, $t0
addi $sp, $sp, -4
sw $a0, 0($sp)
# Guardando $a0-$a3 del llamador antes de la llamada a fib
addi $sp, $sp, -16
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $a2, 8($sp)
sw $a3, 12($sp)
lw $a0, -12($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0, 2
lw $t1, 0($sp)
addi $sp, $sp, 4
subu $a0, $t1, $a0
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, 0($sp)
addi $sp, $sp, 4
jal fib
move $t0, $v0
# Restaurando $a0-$a3 del llamador después de la llamada a fib
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $a2, 8($sp)
lw $a3, 12($sp)
addi $sp, $sp, 16
move $a0, $t0
lw $t1, 0($sp)
addi $sp, $sp, 4
addu $a0, $t1, $a0
move $v0, $a0
# return statement processed, $v0 holds return value if any. Control flows to epilogue.
endif_5:
endif_3:
move $sp, $fp
lw $ra, -8($fp)
lw $fp, -4($fp)
jr $ra
# función factorial
factorial:
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
addi $fp, $sp, 8
addi $sp, $sp, -4
sw $a0, -12($fp)
lw $a0, -12($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0, 0
lw $t1, 0($sp)
addi $sp, $sp, 4
seq $a0, $t1, $a0
beqz $a0, else_6
li $a0, 1
move $v0, $a0
# return statement processed, $v0 holds return value if any. Control flows to epilogue.
j endif_7
else_6:
lw $a0, -12($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
# Guardando $a0-$a3 del llamador antes de la llamada a factorial
addi $sp, $sp, -16
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $a2, 8($sp)
sw $a3, 12($sp)
lw $a0, -12($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0, 1
lw $t1, 0($sp)
addi $sp, $sp, 4
subu $a0, $t1, $a0
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, 0($sp)
addi $sp, $sp, 4
jal factorial
move $t0, $v0
# Restaurando $a0-$a3 del llamador después de la llamada a factorial
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $a2, 8($sp)
lw $a3, 12($sp)
addi $sp, $sp, 16
move $a0, $t0
lw $t1, 0($sp)
addi $sp, $sp, 4
mul $a0, $t1, $a0
move $v0, $a0
# return statement processed, $v0 holds return value if any. Control flows to epilogue.
endif_7:
move $sp, $fp
lw $ra, -8($fp)
lw $fp, -4($fp)
jr $ra
# función main
main:
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
addi $fp, $sp, 8
addi $sp, $sp, -16
li $v0, 5
syscall
move $a0, $v0
sw $a0, -12($fp)
lw $a0, -12($fp)
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall
lw $a0, -12($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0, 2
lw $t1, 0($sp)
addi $sp, $sp, 4
addu $a0, $t1, $a0
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, 0($sp)
sw $a0, -16($fp)
addi $sp, $sp, 4
# Guardando $a0-$a3 del llamador antes de la llamada a gcd
addi $sp, $sp, -16
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $a2, 8($sp)
sw $a3, 12($sp)
lw $a0, -16($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, -12($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, 4($sp)
lw $a1, 0($sp)
addi $sp, $sp, 8
jal gcd
move $t0, $v0
# Restaurando $a0-$a3 del llamador después de la llamada a gcd
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $a2, 8($sp)
lw $a3, 12($sp)
addi $sp, $sp, 16
move $a0, $t0
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall
# Guardando $a0-$a3 del llamador antes de la llamada a fib
addi $sp, $sp, -16
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $a2, 8($sp)
sw $a3, 12($sp)
lw $a0, -12($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, 0($sp)
addi $sp, $sp, 4
jal fib
move $t0, $v0
# Restaurando $a0-$a3 del llamador después de la llamada a fib
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $a2, 8($sp)
lw $a3, 12($sp)
addi $sp, $sp, 16
move $a0, $t0
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall
# Guardando $a0-$a3 del llamador antes de la llamada a factorial
addi $sp, $sp, -16
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $a2, 8($sp)
sw $a3, 12($sp)
lw $a0, -12($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, 0($sp)
addi $sp, $sp, 4
jal factorial
move $t0, $v0
# Restaurando $a0-$a3 del llamador después de la llamada a factorial
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $a2, 8($sp)
lw $a3, 12($sp)
addi $sp, $sp, 16
move $a0, $t0
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall
li $a0, 0
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, 0($sp)
sw $a0, -24($fp)
addi $sp, $sp, 4
while_start_8:
lw $a0, -24($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, -12($fp)
lw $t1, 0($sp)
addi $sp, $sp, 4
slt $a0, $t1, $a0
beqz $a0, while_end_9
lw $a0, -24($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, -24($fp)
lw $t1, 0($sp)
addi $sp, $sp, 4
mul $a0, $t1, $a0
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, 0($sp)
sw $a0, -20($fp)
addi $sp, $sp, 4
lw $a0, -20($fp)
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall
lw $a0, -24($fp)
addi $sp, $sp, -4
sw $a0, 0($sp)
li $a0, 1
lw $t1, 0($sp)
addi $sp, $sp, 4
addu $a0, $t1, $a0
addi $sp, $sp, -4
sw $a0, 0($sp)
lw $a0, 0($sp)
sw $a0, -24($fp)
addi $sp, $sp, 4
j while_start_8
while_end_9:
# final de main
li $v0, 10
syscall
