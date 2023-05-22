G = {} 
C = {}
I = {}
J = {}
A = {}
AG = {}
inputstring = ""
start = ""
start1 = ""
terminals = []
nonterminals = []
symbols = []
error = 0
relation = []
r1 = []
n = int(input("Enter no of productions: ")) 
entry = ""
def parse_grammar():
    global G, start, terminals, nonterminals, symbols, entry
    for i in range(n):
        x = input() 

        line = " ".join(x.split())

        if(line=='\n'):
            break
        
        if i == 0 :
            entry = line[:line.index("->")].strip()
        head = line[:line.index("->")].strip() 
        prods = [l.strip().split(' ') for l in ''.join(line[line.index("->")+2:]).split('|')] 
        

        if not start:
            start = head+"'" 
            AG[start] = [[head]]
            nonterminals.append(start)


        if head not in G: 
            AG[head] = []
            G[head] = []


        if head not in nonterminals: 
            nonterminals.append(head)


        for prod in prods:
            G[head].append(prod) 
            AG[head].append(prod)

            for char in prod:
                if not char.isupper() and char not in terminals:
                    terminals.append(char)

                elif char.isupper() and char not in nonterminals:
                    nonterminals.append(char)

                    G[char] = [] 
                    A[char] = []
                    AG[char] = []
    symbols = terminals+nonterminals

    

first_look = []


def first(X):
    if X in terminals:
        return [X]
    first_l = []
    for prods in G[X]:
        if prods[0] in terminals or prods[0] == '':
            if prods[0] not in first_l:
                first_l.append(prods[0])
        else:
            
            for i in range(len(prods)):
                if prods[i] in terminals or prods[i] == '':
                    if prods[i] not in first_l:
                        first_l.append(prods[i])
                    break
                else:
                    if i == len(prods) - 1:
                        for terms in first(prods[i]):
                            if terms not in first_l:
                                first_l.append(terms)
                    else:
                        for terms in first(prods[i]):
                            if terms not in first_l:
                                first_l.append(terms)
                        if '' not in first_l:
                            break
                        else:
                            first_l.remove('')
    return first_l

def follow(A):
    global entry
    follow_l = set()
    if A == entry:
        follow_l.update('$')
    global nonterminals
    for heads in G.keys():
        for prods in G[heads]:
            for i in range(len(prods)):
                if prods[i] == A:
                    if i == len(prods) - 1 and heads != A:
                        follow_l.update(follow(heads))
                    else:
                        if i + 1 < len(prods):
                            if(prods[i+1] in nonterminals):
                                j = i + 1
                                while j < len(prods):
                                    if prods[j] in nonterminals:
                                        follow_l.update(first(prods[j]))
                                        if '' not in follow_l:
                                            break 
                                        else:
                                            if j == len(prods) - 1 and prods[j] != heads:
                                                follow_l.update(follow(heads))
                                            follow_l.discard('')
                                    else:
                                        follow_l.update(prods[j])
                                        break
                                    j += 1
                            else:
                                follow_l.update(prods[i+1])
                                #break
    
    return follow_l

#Funcion para obtener Closure
def closure(I):
    #Se recibe la produccion a la que se le sacara el closure
    J = I 
    while True:
        #Se recorre la(s) producciones
        item_len = len(J)+sum(len(v) for k, v in J.items())
        for heads in list(J): 
            for prods in J[heads]: 
                dot_pos = prods.index('.')
                if prods == '.':
                    continue
                #Si el punto no esta al final
                if dot_pos+1 < len(prods): 
                    prod_after_dot = prods[dot_pos+1]
                    #Si el siguiente es no terminal
                    if prod_after_dot in nonterminals:
                        #Para cada produccion de ese no-terminal se agregar el punto al inicio
                        for prod in AG[prod_after_dot]: 
                            item = ["."]+prod 
                            #Si el no terminal no esta en el closure actual, se agrega
                            if prod_after_dot not in J.keys():
                                J.update({prod_after_dot:[item]})
                            elif item not in J[prod_after_dot]:
                                J[prod_after_dot].append(item) 

        if item_len==len(J)+sum(len(v) for c, v in J.items()):
            return J

#Funcion para obtener el GOTO
def Goto(I, X):
    #Esta funcion recibe el estado y el simbolo al que se puede hacer el GOTO
    goto = {}
    #Se recorre las producciones que hay en el estado recibido
    for heads, t in I.items():
        for prods in I[heads]:
            for i in range(len(prods)-1):
                #Si luego del punto esta el simbolo objetivo
                if "."==prods[i] and X == prods[i+1]:
                    #Se pasa el punto, y se crea el closure de esa transicion
                    temp_prods = prods[:]
                    temp_prods[i], temp_prods[i+1] = temp_prods[i+1], temp_prods[i]
                    prod_closure = closure({heads: [temp_prods]})
                    #Luego, se recorre las producciones del closure creado
                    for keys, v in prod_closure.items():
                        #Se anaden estas al goto si no estan
                        if keys not in goto.keys():
                            goto[keys] = prod_closure[keys]
                        elif prod_closure[keys] not in goto[keys]:
                            goto[keys].append(prod_closure[keys][0])
    return goto


#Esta funcion permite sacar todos los items (estados) del analizador
def items():
    global C
    i = 1
    #Se genera el estado cero mediante el closure
    C = {'I0': closure({start: [['.']+AG[start][0]]})}
    while True:
        item_len = len(C) + sum(len(v) for k, v in C.items())
        #Se recorre cada item creado, y luego cada simbolo
        for I in list(C):
            for X in symbols:
                #Si el simbolo no es epsilon, se mira si se puede hacer un GOTO entre este estado y el simbolo que se evaluando a otro
                if '' != X :
                    if Goto(C[I], X) and Goto(C[I], X) not in C.values():
                        #Si esto ocurre, se crea un nuevo estado
                        C['I'+str(i)] = Goto(C[I], X)
                        i += 1

        if item_len==len(C) + sum(len(v) for k, v in C.items()):
            return


#Funcion para crear la tabla con los actions que puede realizar
proc = {}
def Action(i, a):
    #Esta funcion recibe el estado, y el simbolo para mirar si hay accion entre estos
    global error
    #Se recorre el estado recibido
    for heads in C['I'+str(i)]:
        for prods in C['I'+str(i)][heads]:
            for j in range(len(prods)-1):
                #Si se encuentra, que luego del punto esta el simbolo, hay accion
                if prods[j] == '.' and prods[j+1] == a:
                    for k in range(len(C)):
                        #Se recorre la longitud del estado, y si en un punto existe GOTO entre este estado con el simbolo
                        if Goto(C['I'+str(i)], a)==C['I'+str(k)]:
                            #Si el simbolo esta en terminales, puede hacer un shift
                            if a in terminals:
                                if "r" in parse_table[i][terminals.index(a)] and "r"+str(k) not in proc[(i,terminals.index(a))]:
                                    if error!=1:
                                        print("ERROR: Shift-Reduce Conflict at State "+str(i)+", Symbol \'", str(terminals.index(a))+"\'")
                                    error = 1

                                    if "s"+str(k) not in parse_table[i][terminals.index(a)] :

                                        parse_table[i][terminals.index(a)] = parse_table[i][terminals.index(a)]+"/s"+str(k)
                                    elif "r"+str(k) not in parse_table[i][terminals.index(a)]:
                                        parse_table[i][terminals.index(a)] = parse_table[i][terminals.index(a)]+"/r"+str(k)
                                    return parse_table[i][terminals.index(a)]
                                else:
                                    if (i,terminals.index(a)) in proc:
                                        proc[(i,terminals.index(a))].append("s"+str(k))
                                    else:
                                        proc[(i,terminals.index(a))] = []
                                        proc[(i,terminals.index(a))].append("s"+str(k))
                                        parse_table[i][terminals.index(a)] = "s"+str(k)
                            else:
                                parse_table[i][len(terminals)+nonterminals.index(a)] = str(k)
                            
                            return "s"+str(k)
    cont = 0
    #Si no retorno en lo anterior, puede haber un reduce, entonces se recorre el estados
    for heads in C['I'+str(i)]:
        if heads != start:
            for prods in C['I'+str(i)][heads]:
                #Si el punto esta de ultimo o es cadena vacia
                if prods[-1] == '.'  or prods[-1] == '': 
                    k = 0
                    #Se busca por la produccion en la gramatica
                    for head, tail in AG.items():
                        for gprods in AG[head]:
                            global z
                            #Una vez se encuentra la produccion, se toman los terminos del follow del noterminal de la produccion, y se anade el reduce a estos
                            if (head == heads and (gprods == prods[:-1]) and (a in terminals or a == '$')) or (head == heads and prods[-1] == '' and gprods == ['']):
                                for terms in follow(heads):

                                    if terms == '$':
                                        index = len(terminals)
                                    else:
                                        index = terminals.index(terms)
                                    if "s" in parse_table[i][index] and "r"+str(k) not in proc[(i,index)]:
                                        if error!=1:
                                            print("ERROR: Shift-Reduce conflict at state "+str(i)+", Symbol \'"+str(terms)+"\'")
                                        error = 1

                                        if "r"+str(k) not in parse_table[i][index]:
                                            parse_table[i][index] = parse_table[i][index]+"/r"+str(k)
                                        elif "s"+str(k) not in parse_table[i][index]:
                                            parse_table[i][index] = parse_table[i][index]+"/s"+str(k)
                                        return parse_table[i][index]
                                    
                                    elif parse_table[i][index] and "r"+str(k) not in proc[(i,index)]:
                                        if error!=1:
                                            print("ERROR: Reduce-Reduce conflict at state "+str(i)+", Symbol \'"+str(terms)+"\'")
                                        error = 1
                                        if "r"+str(k) not in parse_table[i][index]:
                                            parse_table[i][index] = parse_table[i][index]+"/r"+str(k)
                                       
                                        return parse_table[i][index]

                                    else:
                                        if (i,index) in proc:
                                            proc[(i,index)].append("r"+str(k))
                                        else:
                                            proc[(i,index)] = []
                                            proc[(i,index)].append("r"+str(k))
                                        parse_table[i][index] = "r"+str(k)
                                
                                if cont == len(C['I'+str(i)])-1:
                                    return "r"+str(k)
                            

                            k += 1
        cont +=1
    
    if start in C['I'+str(i)] and AG[start][0] + ['.'] in C['I'+str(i)][start]:
        parse_table[i][len(terminals)] = "accept"

        return "accept"

    return ""

def print_info():

    print("\nGRAMMAR:")

    for head, tail in G.items():
        if head==start:
            continue

        print(head, " ->", end=" ")

        for t in tail:
            for r in t:
                print(r, end=" ")

            if(t!=tail[len(tail)-1]):
                print(" |", end=" ")
        print()

    print("\nAugmented Grammar:")

    for head, tail in AG.items():
        print(head, " ->", end=" ")
        for t in tail:
            for r in t:
                print(r, end=" ")

            if(t!=tail[len(tail)-1]):
                print(" |", end=" ")
        print()
    
    print("\nTerminals: ", terminals)

    print("\nNon-terminals: ", nonterminals)

    print("\nSymbols: ", symbols)

    print("\nFirst:")

    for head, t in G.items():

        print("First("+head+"): {", end="")
        fir = first(head)
        firf = []
        firf.extend(fir)
        for v in firf:
            print(v, end="")

            if v!=firf[-1]:
                print(", ", end="")
        print("}")
    print("\nFollow:")
    global z
    for f, t in G.items():
        print("Follow("+f+"): {", end="")   
        fir = follow(f)
        firf = []
        firf.extend(fir)
        for v in firf:
            print(v, end="")

            if v!=firf[-1]:
                print(", ", end="")
        print("}")

    print("\nItems:")

    for i in range(len(C)):

        print('I'+str(i)+':')
        for keys in C['I'+str(i)]:
            for prods in C['I'+str(i)][keys]:
                print(keys, " -> ", end=" ")
                for prod in prods:
                    print(prod, end=" ")
                print()
        print()

    print("\nClosure:")

    for h1, t1 in C.items():

        print(h1, ":")
        for head, tail in t1.items():
            print(head, " ->", end=" ")
            for t in tail:
                for r in t:
                    print(r, end=" ")

                if(t!=tail[len(tail)-1]):
                    print(" |", end=" ")
            print()
        print()

    for i in range(len(parse_table)): 
        for j in symbols:
            if j != '':
                Action(i, j)
                    

    print("\nParsing Table:")
    print("+"+"--------+"*(len(terminals)+len(nonterminals)+1))
    print("{:^8} |".format('STATE'), end="")

    for terms in terminals:
        print("{:^7}|".format(terms), end="")
    print("{:^7}|".format("$"), end="")

    for nont in nonterminals:
        if nont == start:
            continue
        print("{:^7}|".format(nont), end="")

    print("\n+" + "--------+"*(len(terminals)+len(nonterminals)+1))

    for i in range(len(parse_table)):
        print("|{:^8}|".format(i), end="")
        for j in range(len(parse_table[i])-1):
            print("{:^7}|".format(parse_table[i][j]), end="")
        print()

    print("+"+"--------+"*(len(terminals)+len(nonterminals)+1))

def process_input():
    input_str = input("\nEnter input of string: ")
    while input_str != '0':
    
        parse_str = " ".join((input_str+" $").split()).split(" ")
        pointer = 0
        stack = ['0']

        print("\n+--------+----------------------------+----------------------------+-------------------------------+")
        print("|{:^8}|{:^28}|{:^28}|{:^31}|".format("STEP", "STACK", "INPUT", "ACTION"))
        print("+--------+----------------------------+----------------------------+-------------------------------+")

        step = 1

        while(True):
            curr_sym = parse_str[pointer]
            st_top = int(stack[-1])
            stackBody = ""
            inputBody = ""

            print("|{:^8}|".format(step), end="")

            for i in stack:
                stackBody += i
                if i!=stack[-1]:
                    stackBody += " "

            print("{:^28}|".format(stackBody), end="")

            i = pointer

            while(i<len(parse_str)):
                inputBody += parse_str[i]
                i += 1

            print("{:^27} | ".format(inputBody), end="")
            step += 1
            #Se obtiene la accion a realizar
            if curr_sym == '$':
                getAct = parse_table[st_top][len(terminals)]
            else:
                getAct = parse_table[st_top][terminals.index(curr_sym)]

            #Si la accion contiene / , hay un error
            if "/" in getAct:
                print("{:^30}|".format(getAct+". So conflict"))
                break
            
            #Si la accion contiene s, es un shift,m entonces se agrega a la pila, y se pasa de caracter en la cadena
            if "s" in getAct:
                print("{:^29} |".format(getAct))
                stack.append(getAct[1:])
                
                pointer += 1
            #Si es reduce, se recorre la gramatica en busqueda de la produccion, y se saca de la pila, la longitud de esa produccion
            #Luego, se ingresa en la pila, el GOTO, entre el top y el simbolo
            elif "r" in getAct:
                print("{:^29} |".format(getAct))
                i = 0
                for head, tail in AG.items():
                    for prods in AG[head]:
                        if prods[-1] == '' and i == int(getAct[1:]): 
                            
                            state = stack[-1]
                            stack.append(parse_table[int(state)][len(terminals)+nonterminals.index(head)])
                            
                        elif i == int(getAct[1:]):
                            for j in range(len(prods)):
                                stack.pop()
                            state = stack[-1]
                            stack.append(parse_table[int(state)][len(terminals)+nonterminals.index(head)])
                            
                        i += 1

            elif getAct == "accept" and pointer == len(parse_str) - 1:
                print("{:^29} |".format("ACCEPTED"))
                break

            else:
                print("ERROR: Unrecognized symbol", curr_sym, "|")
                break

        print("+--------+----------------------------+----------------------------+-------------------------------+")
        input_str = input("\nEnter input of string: ")
        
    
parse_grammar()

C = {'I0':closure({start:[['.']+AG[start][0]]})}

for X in symbols:
    I = C['I0']

Goto(C['I0'], "A")

items()

global parse_table

parse_table = [["" for c in range(len(terminals)+len(nonterminals)+1)] for r in range(len(C))]

print_info()

process_input()
