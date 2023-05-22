# Proyecto final

## Descripción:

El presente código consiste en la implementación de dos analizadores sintáctivos en Python, el primero de ellos es LL(1) y el segundo es un analizador SLR(1).

Los componentes del analizador LL(1) son:

-First del conjunto de los no terminales y terminales.
-First de una cadena compuesta por terminales y no terminales.
-Follow de los no terminales.
-Tabla de analisis sintáctico.
-Analizador de cadenas pertenecientes a la gramática.

(Como especificación el parser no recibe gramáticas con ningún tipo de recursión izquierda)


Los componentes del analizador SLR(1) son:
-First y follow de la gramática.
-Clousure de los elementos de la gramática.
-Goto de las tablas generadas por la gramática.
-El conjunto de items derivados del clousure.
-Action de las tablas generadas.
-Analizador de las cadenas pertenecientes a la gramática.
-Tabla de análisis sintáctico.
