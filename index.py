def permutacoes(maxi):
    def multiplicacao(x):
        res = 1
        for i in x:
            res *= i
        return res
    listas = []
    m = len(maxi)
    ini = [0 for i in range(m)]
    ant = ini
    listas.append(ini.copy())
    for i in range(1,multiplicacao(maxi)):
        for j in range(m):
            if j < m-1:
                if i%maxi[j+1] == 0:
                    ant[j] = (ant[j] + 1)%maxi[j]
            else:
                ant[j] = (ant[j] + 1) % maxi[j]
        #print(ant)
        listas.append(ant.copy())
    return listas



