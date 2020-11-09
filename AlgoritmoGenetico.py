from random import sample
from math import sqrt
from numpy import array
from numpy import insert
from numpy import reshape
from numpy import random as rd
from numpy import zeros
from numpy import float64
import matplotlib.pyplot as plt


# Aluna: Sara Helena Régis Theiss


###### VARIÁVEIS GLOBAIS

num_genes = 20 # número de genes
tamanho_populacao = 20 # número de cromossomos

x = rd.random_sample(num_genes,)
y = rd.random_sample(num_genes,)

populacao = []

num_interacoes = 10000

taxa_mutacao = 0.05
taxa_selecao = 50

manter_cromossomos = tamanho_populacao * taxa_selecao // 100
m = (tamanho_populacao - manter_cromossomos) // 2
probabilidade = []

menor_custo = 0.0
maior_custo = 0.0


###### FUNÇÕES

def calcula_probabilidades():
    global manter_cromossomos
    global probabilidade

    individuos = manter_cromossomos

    # cria lista de probabilidades, onde o cromossomo com menor 
    # custo ganha 10 chances, o segundo ganha 9, e assim por 
    # diante...
    for i in range(manter_cromossomos):
        for j in range(individuos):
            probabilidade.append(j)
        individuos -= 1

    probabilidade.sort(reverse = True)


def gerar_populacao():
    global num_genes
    global tamanho_populacao
    global populacao

    # gera a população de acordo com o número de cromossomos (caminhos) e o número de genes (cidades)
    for i in range (tamanho_populacao):
        line = sample(range(num_genes), num_genes)
        populacao.append(line)


def cvfun(populacao):
    global x 
    global y

    distancia_cidades = []
    distancia_individuos = []
    
    num_populacao = len(populacao)
    num_cidade = len(populacao[0])

    # adiciona coluna ao final da matriz, com os valores da primeira coluna 
    # (para que a distância considere a volta para o ponto inicial)
    primeira_coluna = array([row[0] for row in populacao]).reshape(20,1)
    tour = insert(populacao, [20], primeira_coluna, axis=1)

    # calcular distância entre as cidades, onde distancia_cidades[i,j] é a distância entre i e j
    #    * quando i é igual a j, distancia_cidades[i,j] = 0
    #   ** distancia_cidades[i,j] = distancia_cidades[j,i]
    for i in range(num_cidade):
        line = []
        for j in range(num_cidade):
            line.append(round(sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2),2))
        distancia_cidades.append(line)

    soma = 0

    # calcula a distância total para cada cromossomo (soma a distância entre os indivíduos)
    for i in range(num_populacao):
        for j in range(num_cidade):
            soma += distancia_cidades[ tour[i][j] ][ tour[i][j+1] ]
        distancia_individuos.append(soma)
        soma = 0
    
    return distancia_individuos


###### MAIN

calcula_probabilidades()

gerar_populacao()

# calcula custos dos cromossomos
dist = cvfun(populacao)

# salva menor e maior custo
menor_custo = min(dist)
maior_custo = max(dist)

# ordena população da menor para a maior distância
populacao = [x for y, x in sorted(zip(dist, populacao))]

for contador in range(num_interacoes):
    escolha_1 = sample(range(len(probabilidade)), m)
    escolha_2 = sample(range(len(probabilidade)), m)

    # crossover
    for i in range(m):
        # escolhe os dois cromossomos que serão os pais, de acordo com as probabilidades
        pai_1 = populacao[probabilidade[escolha_1[i]]].copy()
        pai_2 = populacao[probabilidade[escolha_2[i]]].copy()
        indx = 2 * i + 1
        pos_atual = rd.randint(num_genes)

        salva_pai = pai_1.copy()
        pos_ini = pos_atual
        while True:
            # troca o valor que está no pai 1 pelo que está no pai 2 e vice-versa
            pai_1[pos_atual] = pai_2[pos_atual]
            pai_2[pos_atual] = salva_pai[pos_atual]

            # quando o valor trocado for igual ao primeiro valor trocado no  início, significa que não há mais valores duplicados
            if pai_1[pos_atual] == salva_pai[pos_ini]:
                break

            pos_atual = salva_pai.index(pai_1[pos_atual])
        
        # atribui os filhos gerados à população
        populacao[manter_cromossomos - 1 + indx] = pai_1
        populacao[manter_cromossomos - 1 + indx + 1] = pai_2


    mutacao = int(tamanho_populacao * num_genes * taxa_mutacao)

    # mutação
    for i in range(mutacao):
        # pega dois indíviduos aleatórios de um cromossomo aleatório
        linha = rd.randint(manter_cromossomos, tamanho_populacao)
        individuo_1 = rd.randint(num_genes)
        individuo_2 = rd.randint(num_genes)

        # troca os indivíduos de posição para fazer a mutação
        salva_ind = populacao[linha][individuo_1]
        populacao[linha][individuo_1] = populacao[linha][individuo_2]
        populacao[linha][individuo_2] = salva_ind

    # calcula custos dos cromossomos
    dist = cvfun(populacao)

    # salva menor e maior custo
    menor_custo = min(dist)
    maior_custo = max(dist)

    # ordena população da menor para a maior distância
    populacao = [x for y, x in sorted(zip(dist, populacao))]


###### RESULTADOS

print("\nRESULTADOS:", end="\n")
print("Tamanho da população: ", tamanho_populacao, end="\n")
print("Taxa de mutação: ", taxa_mutacao, end="\n")
print("Número de cidades: ", num_genes, end="\n")
print("Melhor custo: ", menor_custo, end="\n")
print("Melhor solução:\n", populacao[0], end="\n")


matriz_trajeto_x = zeros([21,1], dtype=float64)
matriz_trajeto_y = zeros([21,1], dtype=float64)

for i in range(20):
    matriz_trajeto_x[i] = x[populacao[0][i]]
    matriz_trajeto_y[i] = y[populacao[0][i]]
    matriz_trajeto_x[20] = x[populacao[0][0]]
    matriz_trajeto_y[20] = y[populacao[0][0]]

plt.figure(3)
plt.plot(matriz_trajeto_x,matriz_trajeto_y)
# label do eixo x
plt.xlabel('Distância X')
# label do eixo y
plt.ylabel('Distância Y')
# label do título
plt.title("Melhor caminho encontrado pelo Algoritmo Genético")

plt.pause(15)
plt.clf()