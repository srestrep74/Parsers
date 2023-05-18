from collections import deque
from copy import deepcopy
from collections import defaultdict

def first(rules,first_dictionary, nonTerminal):
    for prod in rules[nonTerminal]:
        value = prod[0]
        if value not in non_terminals:
            first_dictionary[nonTerminal].update(value)
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


def firstcadena(first_dict, string):
    first_string = set()
    for i in range(len(string)):
        if string[i] in non_terminals:
            first_string.update(first_dict[string[i]])
            if 'e' in first_string:
                first_string.discard()
            else:
                return first_string
        else:
            first_string.update(string[i])
            return first_string



def follow(dict_productions, follow_dictionary, nonTerminal):

    for key in dict_productions:
        for prod in dict_productions[key]:
            for k in range(len(prod)):
                if prod[k]== nonTerminal:
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
                    elif k+1 < len(prod) and prod[k+1] not in non_terminals:
                        follow_dictionary[nonTerminal].update(prod[k+1])

    return follow_dictionary[nonTerminal]

def parsing_table(first_dictionary, follow_dictionary):
    first = deepcopy(first_dictionary)
    follow = deepcopy(follow_dictionary)
    table = defaultdict(list)
    flag = "NO es LL1"
    for non_term,deriv in dict_productions.items():
        for sub_deriv in deriv:
            i = 0
            symbol = sub_deriv[i]
            if symbol in non_terminals:  
                while i < len(sub_deriv):
                    symbol = sub_deriv[i]
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
                        symbol = sub_deriv[i]
                        if {non_term:sub_deriv} not in table[non_term,symbol]:
                            if len(table[non_term,symbol]) == 0:
                                table[non_term,symbol].append({non_term:sub_deriv})
                            else:
                                return flag
                        break
                if  i == len(sub_deriv) and "e" in first_dictionary[symbol]:
                    for ter in follow[non_term]:
                        if {non_term:sub_deriv} not in table[non_term,ter]:
                            if len(table[non_term,ter]) == 0:
                                table[non_term,ter].append({non_term:sub_deriv})
                            else:
                                return flag
            elif symbol == 'e':
                for ter in follow[non_term]:
                    if {non_term:'e'} not in table[non_term,ter]:
                        if len(table[non_term,ter]) == 0:
                            table[non_term,ter].append({non_term:'e'})
                        else:
                           return flag
            else:
                if {non_term:sub_deriv} not in table[non_term,symbol]:
                    if len(table[non_term,symbol]) == 0:
                        table[non_term,symbol].append({non_term:sub_deriv})
                    else:
                        return flag
    return table


def parser2(ini,table):
    expr = list(map(str,input("Ingrese la cadena a evaluar : \n").split())) 
    while expr != []:
        print(elements)
        print("\nLa expresion ingresada es :",expr)
        stack=['$']
        stack.append(ini)
        i=0
        flag = False
        while(stack and expr[i]):
            top = stack[len(stack)-1]
            while top == 'e':
                stack.pop()
                top = stack[len(stack)-1]
            if top == expr[i]:
                if len(stack) == 1 and stack[0] == expr[i]:
                    flag = True
                    break
                stack.pop()
                i += 1
            else:
                if top != 'e' and top in elements:
                    flag = False
                    break
                else:
                    flag = False

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
print(dict_productions)
for k in non_terminals:
    first(dict_productions, first_dictionary, k)

print("\n")
print("First: ",end="\n")
print(first_dictionary)
print("\n")
for h in non_terminals:
    follow(dict_productions,follow_dictionary, h)
print("Follow: ",end="\n")
print(follow_dictionary)
print("\n")
table = parsing_table(first_dictionary, follow_dictionary)
print("Table: ",end="\n")
if table == "ERROR":
    print(table)
else:
    for key in table.keys():
        print(f"{key}:{table[key]}")


t = []
for key,val in table.items():
    t.append([key,val])
parser2(entry,t)
print(firstcadena(first_dictionary, ",SH"))


    