from collections import deque
from copy import deepcopy
from collections import defaultdict


#   Esta función mira el first de todas las producciones de la gramática.


def first(rules,first_dictionary, nonTerminal):
    for prod in rules[nonTerminal]:
        value = prod[0]
        # si en la primer posición de la derivación se encuentra un terminal, agrega el mismo y deja de buscar en la derivación
        if value not in non_terminals:
            first_dictionary[nonTerminal].update(value)
        #en el caso que la derivación comienze con un no terminal, agrega el first del mismo; pero si el no terminal deriva en la cadena vacía, entonces recorrerá la derivación hasta que se encuentre
        #con un símbolo diferente de la cadena de la vacia, pero si al llegar al final de la producción siempre está la cadena vacía entonces esta será agregada al first.
        else:
            i=0
            cante = 0
            while i<len(prod):
                if prod[i] not in non_terminals:
                    first_dictionary[nonTerminal].update(prod[i])
                    break
                else:

                    temp = first(rules, first_dictionary, prod[i])
                    if "e" not in first_dictionary[prod[i]]:
                        first_dictionary[nonTerminal].update(temp)
                        break
                    else:
                        cante+=1
                        temp.discard("e")
                        first_dictionary[nonTerminal].update(temp)
                        if cante == len(prod):
                            temp.update("e")
                            first_dictionary[nonTerminal].update(temp)
                       
                i+=1
            
            
    return first_dictionary[nonTerminal]

#   Esta función se encarga de sacar el fist de una cadena específica, se cumple la condición de que si la cadena empieza con un terminal, entonces el first será ese terminal, si es
#un no terminal el first será el first de las derivaciones del no terminal, si todas las derivaciones de la cadena contienen la cadena vacía, entonces el first de la cadena también 
#lo tendrá.

def firstcadena(first_dict, string):
    first_string = set()
    for i in range(len(string)):
        if string[i] in non_terminals:
            first_string.update(first_dict[string[i]])
            if 'e' in first_string:
                first_string.discard('e')
            else:
                return first_string
        else:
            first_string.update(string[i])
            return first_string

#   Esta función mira si la gramática es LL1, lo que hace es que mira las derivaciones de un mismo no terminal y las interseca, si la interseccion es diferente al conjunto vacío
#entonces la gramática no será LL1.

def isLL1(first_dict, rules):
    for non_term in rules.keys():
        for i in range(len(rules[non_term])): #alpha
            for j in range(i+1,len(rules[non_term])): #beta
                set1 = set()
                set2 = set()
                set1.update(firstcadena(first_dict, rules[non_term][i]))
                set2.update(firstcadena(first_dict, rules[non_term][j]))
                inter = set1 & set2
                if len(inter) > 0 :
                    print( f"NO es LL1 : Conflicto entre {rules[non_term][i]} , {rules[non_term][j]}")
                    return True

#   Esta función busca el follow de todos los no terminales. 

def follow(dict_productions, follow_dictionary, nonTerminal):

    for key in dict_productions:
        for prod in dict_productions[key]:
            for k in range(len(prod)):
                if prod[k]== nonTerminal:
                    

#si el siguiente es un no terminal entonces se agrega el first del mismo hasta que no contenga 
#la cadena vacia, si el siguiente es un terminal se agrega al follow ese terminal.

                    if k== len(prod)-1 and prod[k]!= key:
                        
                        follow_dictionary[nonTerminal].update(follow( dict_productions,follow_dictionary, key))
                    elif k+1 < len(prod) and prod[k+1].isupper():
                        i = k+1
                        while i<len(prod):
                            if(prod[i].isupper()):
                                if i<len(prod):
                                    
                                    follow_dictionary[nonTerminal].update(first_dictionary[prod[i]])
                                    if "e" in first_dictionary[prod[i]]:
                                        follow_dictionary[nonTerminal].discard("e")
                                        if i== len(prod)-1:
                                            follow_dictionary[nonTerminal].update(follow(dict_productions, follow_dictionary, key))
                                    else:
                                        break      
                            
                            else:
                                follow_dictionary[nonTerminal].update(prod[i])
                                
                            i+=1
                    #Busca el no terminal en las derivaciones y verifica el elemento al lado del mismo, si resulta que el no terminal buscado
                     #se encuentra en el final de la derivación entonces se agrega el follow de la key en la que se encuentra
                    elif k+1 < len(prod) and prod[k+1] not in non_terminals:
                        follow_dictionary[nonTerminal].update(prod[k+1])

    return follow_dictionary[nonTerminal]


#Esta funcion genera la tabla
def parsing_table(first_dictionary, follow_dictionary):
    first = deepcopy(first_dictionary)
    follow = deepcopy(follow_dictionary)
    table = defaultdict(list)
    flag = "NO es LL1"
    #Se recorre cada produccion de la gramatica
    for non_term,deriv in dict_productions.items():
        for sub_deriv in deriv:
            i = 0
            #Se guarda el simbolo inicial de la produccion
            symbol = sub_deriv[i]
            #Si el simbolo esta en no-terminales
            if symbol in non_terminals:  
                while i < len(sub_deriv):
                    symbol = sub_deriv[i]
                    #Si el simbolo es un no-terminal y esta el epsilon en first, se anade la produccion a cada simbolo del first en la tabla sin el epsilon 
                    if symbol in non_terminals:
                        if "e" in first_dictionary[symbol]:
                            for ter in first[symbol]-{"e"}:
                                if {non_term:sub_deriv} not in table[non_term,ter]:
                                    if len(table[non_term,ter]) == 0:
                                        table[non_term,ter].append({non_term:sub_deriv})
                                    else:
                                        return flag
                            i += 1
                        else:
                            for ter in first[symbol]-{"e"}:
                                if {non_term:sub_deriv} not in table[non_term,ter]:
                                    if len(table[non_term,ter]) == 0:
                                        table[non_term,ter].append({non_term:sub_deriv})
                                    else:
                                        return flag
                            break
                    else:
                        #Si es un terminal, solo se anade la produccion que genera a este en la tabla
                        symbol = sub_deriv[i]
                        if {non_term:sub_deriv} not in table[non_term,symbol]:
                            if len(table[non_term,symbol]) == 0:
                                table[non_term,symbol].append({non_term:sub_deriv})
                            else:
                                return flag
                        break
                #Si se esta al final de la produccion, y e esta en el first, se anade que se puede ir a cada symbolo del follow con e
                if  i == len(sub_deriv) and "e" in first_dictionary[symbol]:
                    for ter in follow[non_term]:
                        if {non_term:sub_deriv} not in table[non_term,ter]:
                            if len(table[non_term,ter]) == 0:
                                table[non_term,ter].append({non_term:sub_deriv})
                            else:
                                return flag
            #Si el simbolo es e, se anade la transicion a cada symbolo del follow, con e
            elif symbol == 'e':
                for ter in follow[non_term]:
                    if {non_term:'e'} not in table[non_term,ter]:
                        if len(table[non_term,ter]) == 0:
                            table[non_term,ter].append({non_term:'e'})
                        else:
                           return flag
            #Sino, es terminal, y se anade su produccion en la tabla
            else:
                if {non_term:sub_deriv} not in table[non_term,symbol]:
                    if len(table[non_term,symbol]) == 0:
                        table[non_term,symbol].append({non_term:sub_deriv})
                    else:
                        return flag
    return table


# Esta función verifica si se puede o no procesar una cadena con la gramática
def parser2(ini,table):
    #se guarda la cadena como una lista
    expr = list(map(str,input("Ingrese la cadena a evaluar : \n").split())) 

    while expr != []:
        print(elements)
        print("\nLa expresion ingresada es :",expr)
        #sea agrega $ al stack y el símbolo inicial
        stack=['$']
        stack.append(ini)
        i=0
        flag = False
        while(stack and expr[i]):
            #si el top de la pila es la cadena vacia los saca
            top = stack[len(stack)-1]
            while top == 'e':
                stack.pop()
                top = stack[len(stack)-1]

            #si el top de la pila es el terminal que se procesa en la cadena se saca
            if top == expr[i]:
                #si el top de la pila es $ y también lo es el elemento procesado de la cadena la cadena es válida
                if len(stack) == 1 and stack[0] == expr[i]:
                    flag = True
                    break
                stack.pop()
                i += 1
            else:
                #si el top de la pila es un terminal y no coincide con el evaluado en la cadena, la cadena no es válida
                if top != 'e' and top in elements:
                    flag = False
                    break
                else:
                    flag = False

                    #se busca la derivacion del no terminal en la gramatica y se añade la derivación a la pila
                    for x in table:
                        if x[0] == (top,expr[i]): 
                        
                            flag  = True
                            deriv = x[1][0][top]
                            stack.pop()
                            for k in range(len(deriv)):
                                if(k != 'e'):
                                    stack.append(deriv[-k-1])
                            break

                    if flag == False:
                        break
        if flag:
                print("\nExpresion aceptada")
        else:
            print("\nExpresion rechazada, no puede ser aceptada por esta gramatica")
        expr = list(map(str,input("Ingrese la cadena a evaluar : \n").split()))
                    


dict_productions = {}
first_dictionary = {}
follow_dictionary = {}

non_terminals = []
elements=[]
entry = ""

for i in elements:
    first_dictionary[i] = set()
    follow_dictionary[i] = set()


dict_productions = {}

n_productions = int(input('Enter the number of productions :'))
for i in range(n_productions):
    x = input() #read productions from input
    symb, nont = x.split(" -> ")
    if i == 0 :
        entry = symb
    if symb not in dict_productions:
        dict_productions[symb] = []
        non_terminals.append(symb)
    dict_productions[symb].append(nont)

for key in dict_productions:
    for prods in range(len(dict_productions[key])):
        for k in range(len(dict_productions[key][prods])):
            if dict_productions[key][prods][k] not in non_terminals and dict_productions[key][prods][k] not in elements:
                elements.append(dict_productions[key][prods][k])
                if dict_productions[key][prods][k] != 'e':
                 first_dictionary[dict_productions[key][prods][k]] = {dict_productions[key][prods][k]}

for i in non_terminals:
    first_dictionary[i] = set()
    follow_dictionary[i] = set()

print("\n")
print("Non-Terminals: ",end="\n")
print(non_terminals)
print("\n")
print("Terminals: ",end="\n")
print(elements)

follow_dictionary[entry] = {"$"}
for k in non_terminals:
    first(dict_productions, first_dictionary, k)

print("\n")
print("First: ",end="\n")
print(first_dictionary)
print("\n")
for h in non_terminals:
    follow(dict_productions,follow_dictionary, h)

#Es LL1
flag = isLL1(first_dictionary, dict_productions)
if flag != True:

    print("Follow: ",end="\n")
    print(follow_dictionary)
    print("\n")
    table = parsing_table(first_dictionary, follow_dictionary)
    print("Table: ",end="\n")
    if table == "NO es LL1":
        print(table)
    else:
        for key in table.keys():
            print(f"{key}:{table[key]}")


    t = []
    for key,val in table.items():
        t.append([key,val])
    parser2(entry,t)
    print(firstcadena(first_dictionary, ",SH"))
