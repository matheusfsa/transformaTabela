from index import permutacoes
import pickle

class Variable(object):
    "A discrete random variable; conditional on zero or more parent Variables."

    def __init__(self, name, domain, parents):
        "A variable has a name, list of parent variables, and a Conditional Probability Table."
        self.__name__ = name
        self.parents = parents
        self.domain = domain

    def __repr__(self): return self.__name__

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
arquivo = input("Nome do arquivo de saida:")
lookup_name = input("Nome do arquivo lookup:")
saida = open(arquivo, "a")
s_n = input("Tem arquivo lookup?(s/n)")
temLookup = True if s_n == "s" else False
temTabela = True
variaveis = []
lookup = {}
if temLookup:
    with open(lookup_name, 'rb') as entrada:
        lookup = pickle.load(entrada)
        print(lookup)
res = ""
while temTabela:
    variavel = input("Nome da variável:")

    valores = input("Valores possíveis(separados por espaço): ").split(" ")
    pais = input("Pais da variavel(separados por espaço):")
    var = None
    if pais != "-1":
        pais = pais.split(" ")
        parents = [lookup[name] for name in pais]
        var = Variable(variavel,valores,parents)
    else:
        pais = None
        var = Variable(variavel, valores, [])
    lookup[variavel] = var
    variaveis.append(var)

    if pais is None:
        builder = "\n.add('" + variavel + "', [], {"
        n = len(valores)-1
        i = 0
        for valor in valores:
            i += 1
            probabilidade = input("Probabilidade do valor "+ valor +":")
            builder += "('"+valor+"'):" + probabilidade
            if i <= n:
                builder += ","
            else:
                builder += "})"
        res += builder
    else:
        builder = "\n.add('" + str(variavel) + "',"+str_lista(parents)+",{"
        vals = [len(v.domain) for v in parents]
        perm = permutacoes(vals)
        max = len(perm)
        k = 0
        for p in perm:
            condicoes = []
            n = len(parents)
            builder += "("
            for i in range(n):
                condicoes.append(parents[i].domain[p[i]])
                builder += "'" + parents[i].domain[p[i]] + "'"
                if i < n-1:
                    builder += ","
                else:
                    builder += "):"
            probabilidades = input("Probabilidades dados " +str(condicoes) + ":").split(" ")
            builder += "ProbDist("
            n = len(valores)
            for i in range(n):
                builder += valores[i] + "=" + probabilidades[i]
                if i < n-1:
                    builder += ","
                else:
                    builder += ")"
            k += 1
            if k < max:
                builder += ","
            else:
                builder += "})"
        res += builder

    s_n = input("Ainda tem tabela?(s/n)")
    temTabela = True if s_n == "s" else False
with open(lookup_name,"wb") as output:
    print(lookup)
    pickle.dump(lookup, output, pickle.HIGHEST_PROTOCOL)
saida.write(res)