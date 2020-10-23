from random import sample
from math import sqrt
from numpy import array
from numpy import insert
from numpy import reshape
from numpy import random as rd

###### VARIÁVEIS GLOBAIS

tam_populacao = 20
num_genes = 20

x = rd.random_sample((20,))
y = rd.random_sample((20,))

###### FUNÇÕES

def dist(populacao):
    global x 
    global y
    global tam_populacao

    # adiciona coluna ao final da matriz, com os valores da primeira coluna 
    # (para que a distância considere a volta para o ponto inicial)
    primeira_coluna = array([row[0] for row in populacao]).reshape(20,1)
    tour = insert(populacao, [20], primeira_coluna, axis=1)

    distancia_cidades = []

    # criar de distância entre as cidades, onde distancia_cidades[i,j] é a distância entre i e j
    #    * quando i é igual a j, distancia_cidades[i,j] = 0
    #   ** distancia_cidades[i,j] = distancia_cidades[j,i]
    for i in range(tam_populacao):
        line = []
        for j in range(tam_populacao):
            line.append(round(sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2),2)) 
            # V E R I F I C A R -> qnd eu perguntei p a prof se 
            # era feita uma multiplicação entre o x e y com i e j, ela disse que não e 
            # respondeu o que era, mas n deu de entender... 
            # verificar na gravação
        print(line, end="\n")
        distancia_cidades.append(line)

        # % custo de cada cromossomo - a soma das distâncias para cada indivíduo
        # for i=1:Npop
            # dist(i,1)=0;
            # for j=1:Ncidade
                # % Soma das distancias para cada cromossomo
                # dist(i,1)=dist(i)+dcidade(tour(i,j),tour(i,j+1)); 
            # end 
        # end 

def gerar_populacao():
    matriz = []

    for i in range (tam_populacao):
        line = sample(range(tam_populacao), tam_populacao)
        matriz.append(line)
    
    return matriz


###### MAIN

print(x, " - ", y)
dist(gerar_populacao())

