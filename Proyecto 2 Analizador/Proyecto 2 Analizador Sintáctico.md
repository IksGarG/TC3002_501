#### Iker Garcia German
#### Lunes 28 de Abril del 2025
#### Victor Manuel de la Cueva

---
### Gramática (EBNF):
$$
\begin{align*}
\text{program}             &\to \text{declaration‐list} \\[6pt]
\text{declaration‐list}    &\to \{\;\text{declaration}\;\} \\[6pt]
\text{declaration}         &\to \text{var‐declaration} \\
                           &\quad\mid\ \text{fun‐declaration} \\[6pt]
\text{var‐declaration}     &\to \text{type‐specifier}\;\text{ID}\;[\;"["\;\text{NUM}\;"]"\;]\;"\;" \\[6pt]
\text{type‐specifier}      &\to "int" \\
                           &\quad\mid\ "void" \\[6pt]
\text{fun‐declaration}     &\to \text{type‐specifier}\;\text{ID}\;"("\;\text{params}\;")"\;\text{compound‐stmt} \\[6pt]
\text{params}              &\to "void" \\
                           &\quad\mid\ \text{param‐list} \\[6pt]
\text{param‐list}          &\to \text{param}\;\{\;","\;\text{param}\;\} \\[6pt]
\text{param}               &\to \text{type‐specifier}\;\text{ID}\;[\;"["\;"]"\;] \\[6pt]
\text{compound‐stmt}       &\to "{"\;\{\;\text{var‐declaration}\;\}\;\{\;\text{statement}\;\}\;"}" \\[6pt]
\text{statement}           &\to \text{expression‐stmt} \\
                           &\quad\mid\ \text{compound‐stmt} \\
                           &\quad\mid\ \text{selection‐stmt} \\
                           &\quad\mid\ \text{iteration‐stmt} \\
                           &\quad\mid\ \text{return‐stmt} \\
                           &\quad\mid\ \text{input‐stmt} \\
                           &\quad\mid\ \text{output‐stmt} \\[6pt]
\text{expression‐stmt}     &\to [\;\text{expression}\;]\;"\;" \\[6pt]
\text{selection‐stmt}      &\to "if"\;"("\;\text{expression}\;")"\;\text{statement}\;[\;"else"\;\text{statement}\;] \\[6pt]
\text{iteration‐stmt}      &\to "while"\;"("\;\text{expression}\;")"\;\text{statement} \\[6pt]
\text{return‐stmt}         &\to "return"\;[\;\text{expression}\;]\;"\;" \\[6pt]
\text{input‐stmt}          &\to "input"\;"("\;\text{ID}\;")"\;"\;" \\[6pt]
\text{output‐stmt}         &\to "output"\;"("\;\text{expression}\;")"\;"\;" \\[6pt]
\text{expression}          &\to \text{var}\;"="\;\text{expression} \\
                           &\quad\mid\ \text{simple‐expression} \\[6pt]
\text{var}                 &\to \text{ID}\;[\;"["\;\text{expression}\;"]"\;] \\[6pt]
\text{simple‐expression}   &\to \text{additive‐expression}\;[\;\text{relop}\;\text{additive‐expression}\;] \\[6pt]
\text{relop}               &\to "<=" \\
                           &\quad\mid\ "<" \\
                           &\quad\mid\ ">" \\
                           &\quad\mid\ ">=" \\
                           &\quad\mid\ "==" \\
                           &\quad\mid\ "!=" \\[6pt]
\text{additive‐expression} &\to \text{term}\;\{\;\text{addop}\;\text{term}\;\} \\[6pt]
\text{addop}               &\to "+" \\
                           &\quad\mid\ "-" \\[6pt]
\text{term}                &\to \text{factor}\;\{\;\text{mulop}\;\text{factor}\;\} \\[6pt]
\text{mulop}               &\to "*" \\
                           &\quad\mid\ "/" \\[6pt]
\text{factor}              &\to "("\;\text{expression}\;")" \\
                           &\quad\mid\ \text{var} \\
                           &\quad\mid\ \text{call} \\
                           &\quad\mid\ \text{NUM} \\[6pt]
\text{call}                &\to \text{ID}\;"("\;[\;\text{arg‐list}\;]\;")" \\[6pt]
\text{arg‐list}            &\to \text{expression}\;\{\;","\;\text{expression}\;\}
\end{align*}
$$



