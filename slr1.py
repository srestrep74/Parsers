G = {} #productions in list form, augmented grammar
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
        x = input() #read productions from input

        line = " ".join(x.split())

        if(line=='\n'):
            break
        
        if i == 0 :
            entry = line[:line.index("->")].strip()
        head = line[:line.index("->")].strip() 
        prods = [l.strip().split(' ') for l in ''.join(line[line.index("->")+2:]).split('|')] #symbols to right of arrow
        

        if not start:
            start = head+"'" #augmenting the grammar i.e. S'->S
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

                                

def closure(I):
    J = I 
    while True:
        item_len = len(J)+sum(len(v) for k, v in J.items())
        for heads in list(J): #for each key in J
            for prods in J[heads]: #for all prods of key in J
                dot_pos = prods.index('.')
                if prods == '.':
                    continue
                if dot_pos+1 < len(prods): 
                    prod_after_dot = prods[dot_pos+1]
                    if prod_after_dot in nonterminals:
                        for prod in AG[prod_after_dot]: 
                            item = ["."]+prod 

                            if prod_after_dot not in J.keys():
                                J.update({prod_after_dot:[item]})
                            elif item not in J[prod_after_dot]:
                                J[prod_after_dot].append(item) 

        if item_len==len(J)+sum(len(v) for c, v in J.items()):
            return J

def Goto(I, X):

    goto = {}
    for heads, t in I.items():
        for prods in I[heads]:
            for i in range(len(prods)-1):

                if "."==prods[i] and X == prods[i+1]:

                    temp_prods = prods[:]
                    temp_prods[i], temp_prods[i+1] = temp_prods[i+1], temp_prods[i]
                    prod_closure = closure({heads: [temp_prods]})

                    for keys, v in prod_closure.items():

                        if keys not in goto.keys():
                            goto[keys] = prod_closure[keys]
                        elif prod_closure[keys] not in goto[keys]:
                            goto[keys].append(prod_closure[keys][0])
    return goto

def items():

    global C
    i = 1
    C = {'I0': closure({start: [['.']+AG[start][0]]})}

    while True:
        item_len = len(C) + sum(len(v) for k, v in C.items())
        for I in list(C):
            for X in symbols:
                if '' != X :
                    if Goto(C[I], X) and Goto(C[I], X) not in C.values():
                        C['I'+str(i)] = Goto(C[I], X)
                        i += 1

        if item_len==len(C) + sum(len(v) for k, v in C.items()):
            return


def Action2(i,a):
    for heads in C['I'+str(i)]:
        for prods in C['I'+str(i)][heads]:
            for j in range(len(prods)-1):
                if prods[j] == '.' and prods[j+1] == a:
                    for k in range(len(C)):
                        if Goto(C['I'+str(i)], a)==C['I'+str(k)]:
                            if a in terminals:
                                if parse_table[i][terminals.index(a)] == "":
                                    parse_table[i][terminals.index(a)] = "s"+str(k)
                                    return
                                else:
                                    parse_table[i][terminals.index(a)] = parse_table[i][terminals.index(a)]+"/s"+str(k)
                                    print("ERROR: Conflict at State "+str(i)+", Symbol \'", str(terminals.index(a))+"\'")
                                    return
                            else:
                                parse_table[i][len(terminals)+nonterminals.index(a)] = str(k)
                elif (j+1 == len(prods) and prods[j+1] == ".") or (prods[j] == "." and prods[j+1] == ''):
                    cont = 1
                    if start in C['I'+str(i)] and AG[start][0] + ['.'] in C['I'+str(i)][start]:
                        parse_table[i][len(terminals)] = "accept"
                    for key in AG.keys():
                        for gprods in AG[key]:
                            if (key == heads and gprods == prods[:-1] and (a in terminals or a == '$')) or (key == heads and gprods == [''] and prods[-1] == ''):
                                for terms in follow(heads):
                                    if '$' == terms:
                                        parse_table[i][len(terminals)] = "r"+str(cont)
                                        return
                                    elif parse_table[i][terminals.index(terms)] == "":
                                        parse_table[i][terminals.index(terms)] = "r"+str(cont)
                                        return
                                    elif parse_table[i][terminals.index(terms)] != "r"+str(cont):
                                        parse_table[i][terminals.index(terms)] = parse_table[i][terminals.index(terms)]+"/r"+str(cont)
                                        print("ERROR: Conflict at State "+str(i)+", Symbol \'", str(terminals.index(terms))+"\'")
                                        return False
                        cont += 1




proc = {}
def Action(i, a):
    global error
    for heads in C['I'+str(i)]:
        for prods in C['I'+str(i)][heads]:
            for j in range(len(prods)-1):
                if prods[j] == '.' and prods[j+1] == a:
                    for k in range(len(C)):
                        if Goto(C['I'+str(i)], a)==C['I'+str(k)]:
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
    for heads in C['I'+str(i)]:
        if heads != start:
            for prods in C['I'+str(i)][heads]:
                if prods[-1] == '.'  or prods[-1] == '':  #final item
                    k = 0
                    for head, tail in AG.items():
                        for gprods in AG[head]:
                            global z
                            #print(f"{prods[-1]} , {gprods}")
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
            if curr_sym == '$':
                getAct = parse_table[st_top][len(terminals)]
            else:
                getAct = parse_table[st_top][terminals.index(curr_sym)]
            #getAct = Action(st_top, curr_sym)
            if "/" in getAct:
                print("{:^30}|".format(getAct+". So conflict"))
                break

            if "s" in getAct:
                print("{:^29} |".format(getAct))
                #stack.append(curr_sym)
                stack.append(getAct[1:])
                
                pointer += 1

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
                            #stack.append(head)
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
