class Variable(object):
    "A discrete random variable; conditional on zero or more parent Variables."

    def __init__(self, name, domain, parents=()):
        "A variable has a name, list of parent variables, and a Conditional Probability Table."
        self.__name__ = name
        self.parents = parents
        self.domain = domain

    def __repr__(self): return self.__name__


def node(lines, pos,lookup):
    variavel = lines[pos].replace('"', "").replace(",","").replace("  "," ").split(" ")[1]
    linha_valores = lines[pos+1].replace('"', "").replace(",","").replace("  "," ").split(" ")
    print(linha_valores)
    n = int(linha_valores[5])
    valores = linha_valores[9:9+(n)]
    var = Variable(variavel,valores)
    lookup[variavel] = var
    print(variavel, " ", valores)
    return var, pos+3


def multiplicacao(x):
    res = 1
    for i in x:
        res *= i
    return res


def str_lista(lista):
    res = "["
    i = 0
    n = len(lista)
    for el in lista:
        res += "'" + str(el) + "'"
        if i < n-1:
            res += ", "
        i+=1
    res += "]"
    print(res)
    return res

def probability(lines,pos,lookup):
    cabecalho = lines[pos].replace('"', "").replace(",","").replace("  "," ").split(" ")
    print(cabecalho)
    variavel = lookup[cabecalho[2]]
    if len(cabecalho) == 5:
        variavel.parents = []
        builder = "\n.add('" + str(variavel) + "', [], {"
        n = len(variavel.domain)
        lines[pos + 1] = lines[pos + 1].replace('"', "").replace(",","").replace("  "," ").strip("\n")
        lines[pos + 1] = lines[pos + 1].replace(";", "")
        probabilidades = lines[pos+1].split(" ")[2:]
        print(lines[pos+1].split(" "))

        print("Probabilidades: ", probabilidades)
        print(len(variavel.domain))
        print(len(probabilidades))
        i = 0
        for valor in variavel.domain:
            probabilidade = probabilidades[i]
            builder += "('"+valor+"'):" + probabilidade
            if i < n-1:
                builder += ","
            else:
                builder += "})"
            i += 1
        print(builder)
        pos += 3
    else:
        i = 4
        variavel.parents = []
        while cabecalho[i]!=")":
            variavel.parents.append(lookup[cabecalho[i]])
            i += 1
        print(variavel)
        print(variavel.domain)
        print(str_lista(variavel.parents))
        builder = "\n.add('" + str(variavel) + "'," + str_lista(variavel.parents) + ",{"
        vals = [len(v.domain) for v in variavel.parents]
        max = multiplicacao(vals)
        print(max)
        k = 0
        n_parents = len(variavel.parents)
        for i in range(pos+1,pos+1+max):
            condicoes = []
            lines[i] = lines[i].replace('"', "")
            lines[i] = lines[i].replace(",", "")
            lines[i] = lines[i].replace(" (", "")
            lines[i] = lines[i].replace(")", "")
            lines[i] = lines[i].replace(":", "")
            lines[i] = lines[i].replace(";", "")
            lines[i] = lines[i].replace("  ", " ")
            print(lines[i])
            linha = lines[i].strip("\n").split(" ")[1:]
            print(linha)
            builder += "("
            for i in range(n_parents):
                p = int(linha[i])
                condicoes.append(variavel.parents[i].domain[p])
                builder += "'" + variavel.parents[i].domain[p] + "'"
                if i < n_parents - 1:
                    builder += ","
                else:
                    builder += "):"
            probabilidades = linha[n_parents:]
            builder += "ProbDist("
            n = len(variavel.domain)
            for i in range(n):
                builder += variavel.domain[i] + "=" + probabilidades[i]
                if i < n - 1:
                    builder += ","
                else:
                    builder += ")"
            k += 1
            if k < max:
                builder += ","
            else:
                builder += "})"
        pos += max+2
        print(builder)
    return builder,pos

with open("sachs.dsc","r") as file:
    lookup = {}
    lines = file.readlines()
    n = len(lines)
    res = ""
    i = 1
    while i < n:
        if lines[i].startswith('node'):
            var,i = node(lines, i, lookup)
        elif lines[i].startswith('probability'):
            builder, i = probability(lines, i, lookup)
            res += builder
        else:
            print(lines[i])
    with open("asia.out","w") as saida:
        saida.write(res)

