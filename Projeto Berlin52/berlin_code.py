""""berlin52_code"""
import random
import copy
import time
from codigo_teste import main

def achando_posiçoes():
    """ Cria um dicionário de listas com as coordenadas de cada ponto
    Exemplo: 1:[0,10] """
    
   # Linhas abaixo abrem o arquivo transfomando cada linha em um elemento de uma lista,
   # excluindo o cabeçalho.

    arq = open('berlin52.tsp',"r+")
    lista_arq = arq.readlines()
    lista_arq = lista_arq[6:]
    posiçoes = {}

    # laço responsável por limpar as linhas r preencher o dicionário 'posiçoes',
    # com exceção do último, que não tem '\n'.

    for i in range( len(lista_arq) - 1):

        lista = lista_arq[i].split(" ")

        lista[2] = lista[2][0:len(lista[2]) - 1]

        lista = [float(i) for i in lista]

        chave = lista[0]

        lista = lista[1:]

        posiçoes[chave] = lista
    
    # inserem o último elemento no dicionário

    lista = [float(i) for i in lista_arq[len(lista_arq)-1].split(" ")]
    chave = lista[0]
    lista = lista[1:]
    posiçoes[float(chave)] = lista
    
    #função retorna o arquivo e o número de pontos

    arq.close
    n_pontos = len(lista_arq)

    return posiçoes, n_pontos

def caminho_entre(pos_1, pos_2):

    """Função que descobre a distância entre dois pontos"""

    x_1, y_1 = pos_1[0], pos_1[1]
    x_2, y_2 = pos_2[0], pos_2[1]

    diferença_x = abs(x_1 - x_2)
    diferença_y = abs(y_1 - y_2)

    distancia = (diferença_x**2) + (diferença_y**2)
    distancia = distancia**(1/2)
    
    return distancia

def pop_inicial(n_populaçao, n_pontos):

    index = [i for i in range(1, n_pontos + 1)]
    lista = [None] * len(index)
    embaralhado = [None] * (n_populaçao)
    n = len(index) - 1
    count = 0

    while embaralhado[len(embaralhado) - 1] == None:
        a = 0
        while n != -1:
            x =  random.randint(0,n)
            lista[a] = index[x]
            index[x], index[n] = index[n], index[x]
            a+=1
            n-= 1
        embaralhado[count] = lista.copy()
        n = len(index) - 1
        count +=1
    
    return embaralhado

def soma_caminho(caminho,coordenadas):
    soma = 0
    for i in range( len(caminho) - 1):
       soma+= caminho_entre(coordenadas[caminho[i]], coordenadas[caminho[i + 1]])

    soma+= caminho_entre(coordenadas[caminho[len(caminho) - 1]], coordenadas[caminho[0]])
    return caminho, soma

def selecionando(coordenadas,populaçao):

    n = len(populaçao)
    most_fit = [None] * n
    for i in range(n):
        x = random.randint(0,len(populaçao) -2)
        
        caminho_1, distancia_1 = soma_caminho(populaçao[x], coordenadas)
        caminho_2, distancia_2 = soma_caminho(populaçao[x+1], coordenadas)
        
        if distancia_1 < distancia_2:
            most_fit[i] =  caminho_1
        else:
            most_fit[i] = caminho_2
    
    return most_fit

def escolher_pontos_de_corte(tamanho):
    ponto_corte_1 = random.randint(1, tamanho // 2)
    ponto_corte_2 = random.randint(tamanho // 2 + 1, tamanho - 1)
    
    if ponto_corte_1 > ponto_corte_2:
        ponto_corte_1, ponto_corte_2 = ponto_corte_2, ponto_corte_1
    
    return ponto_corte_1, ponto_corte_2

def copiar_subsecoes(pai, ponto_corte_1, ponto_corte_2):
    filho = [None] * int(len(pai))
    filho[ponto_corte_1:ponto_corte_2] = pai[ponto_corte_1:ponto_corte_2]
    return filho

def preencher_filho(filho, pai, ponto_corte_2):
    tamanho = len(filho)
    pos = ponto_corte_2
    for gene in pai:
        if gene not in filho:
            if pos >= tamanho:
                pos = 0
            filho[pos] = gene
            pos += 1
    return filho

def cruzamento(pai_1, pai_2):

    tamanho = int(len(pai_1))
    
    ponto_corte_1, ponto_corte_2 = escolher_pontos_de_corte(tamanho)
    
    filho_1 = copiar_subsecoes(pai_1, ponto_corte_1, ponto_corte_2)
    filho_2 = copiar_subsecoes(pai_2, ponto_corte_1, ponto_corte_2)
    
    filho_1 = preencher_filho(filho_1, pai_2, ponto_corte_2)
    filho_2 = preencher_filho(filho_2, pai_1, ponto_corte_2)

    return filho_1, filho_2

def mutaçao(filho_1, filho_2, p_mutar):

    filhos = [filho_1, filho_2]

    for i in range(len(filhos)):
       chance = random.randint(1,100)
       if chance < p_mutar:
           ponto_mutacao = random.randint(0, len(filhos[i]) - 1)
           primeira_parte = filhos[i][:ponto_mutacao]
           filhos[i][:len(filhos[i]) - ponto_mutacao] = filhos[i][ponto_mutacao:]
           filhos[i][len(filhos[i]) - ponto_mutacao:] = primeira_parte

    return filhos[0], filhos[1]

def distancia_sem_volta(caminho, coordenadas):
    soma = 0
    for i in range( len(caminho) - 1):
       soma+= caminho_entre(coordenadas[caminho[i]], coordenadas[caminho[i + 1]])

    return caminho, soma

def guloso(caminho, coordenadas):

    ponto_corte = random.randint(2, len(caminho)-12)
    corte_2 = ponto_corte + 10

    fragmento_caminho_1, distancia_1 = distancia_sem_volta(caminho[ponto_corte-1:corte_2+1], coordenadas)
    fragmento_caminho_1 = fragmento_caminho_1[1:len(fragmento_caminho_1)-1]

    d_pontos={}
    for i in fragmento_caminho_1:
        d_pontos[i] = [coordenadas[i][0], coordenadas[i][1]]

    caminho_curto, distancia_curta = main( fragmento_caminho_1[0],fragmento_caminho_1, d_pontos, len(fragmento_caminho_1) )
    
    caminho_curto = caminho_curto[:len(caminho_curto)-1]
    caminho_novo = caminho.copy()
    caminho_novo[ponto_corte:corte_2] = caminho_curto

    fragmento_caminho_2, distancia_2 = distancia_sem_volta(caminho_novo[ponto_corte-1:corte_2+1], coordenadas)

    if distancia_2 < distancia_1:
        return caminho_novo
    else:
        return caminho

def crossover(pais,geraçoes, distancias, modelo):
    
    nova_populaçao = [None] * (len(pais))
    for i in range(1, len(pais), 2):

        taxa_crossover = random.randint(1,100)

        if taxa_crossover > modelo["taxa_crossover"]:
        
            filho_1, filho_2 = cruzamento(pais[i],pais[i-1])
        
            filho_1, filho_2 = mutaçao(filho_1, filho_2, modelo["taxa_mutacao"])
        else:
            filho_1, filho_2 = pais[i], pais[i-1]

        if geraçoes != 1 and  geraçoes%20 ==0:
            filho_1 = guloso(filho_1, distancias)

        nova_populaçao[i], nova_populaçao[i-1] = filho_1, filho_2

        if nova_populaçao[len(nova_populaçao)-1] == None:
            nova_populaçao[len(nova_populaçao)-1] = nova_populaçao[len(nova_populaçao)-2]

    return nova_populaçao

def melhor_caminho(coordenadas,populaçao):
    
    menor_caminho, d_menor = soma_caminho(populaçao[0], coordenadas)

    for novo_caminho in populaçao[1:]:
        caminho, distancia = soma_caminho(novo_caminho, coordenadas)
        if distancia < d_menor:
            menor_caminho = caminho
            d_menor = distancia
    
    #menor_caminho.append(menor_caminho[0])

    return menor_caminho, d_menor

def guardando_resultado(caminho, distancia, n_geraçao, nome):

    with open(nome, "a") as arq:

        arq.write("\n")
        arq.write("Geracao numero: " + str(n_geraçao) )
        arq.write("\n")
        for i in range(len(caminho)):
            arq.write(str(caminho[i]))
            if i < len(caminho) - 1:
                arq.write("/")
        
        arq.write("\n")
        
        arq.write(str(distancia))
        arq.write("\n")

def evoluçao(distancias,populaçao,modelo, nome):
    n_geraçoes = 0
    while n_geraçoes< modelo['geracoes'] + 1:

        lista_pais = selecionando(distancias, populaçao)
        filhos = crossover(lista_pais, n_geraçoes, distancias, modelo)

        if n_geraçoes%20 == 0:

            mais_curto, menor_d = melhor_caminho(distancias, populaçao)
            mais_curto = guloso(mais_curto, distancias)
            guardando_resultado(mais_curto, menor_d, n_geraçoes,nome)

        populaçao = filhos
        populaçao[0] = mais_curto
        n_geraçoes+=1
        
    else:
        return mais_curto, menor_d
    
def main_genetico(teste, modelo, nome, tempo):
    
    inicio = time.time()
    
    coordenadas, n_pontos = achando_posiçoes()
    populaçao = pop_inicial(modelo['populacao'], n_pontos)

    with open(nome, "a") as arq:
        arq.write("numero do teste: " + str(teste))
        arq.write("\n")
        arq.write("\n")
    
    mais_curto, menor = evoluçao(coordenadas, populaçao, modelo, nome)
    fim = time.time()

    total = fim - inicio
    with open(nome, "a") as arq:
        arq.write("Tempo de execucao do teste: " + str(total))
        arq.write("\n")
        arq.write("===========================================")
        arq.write('\n')

    tempo += total
    menor += menor
    return tempo, menor

def modelos():
    random.seed(1)  # Define a seed para a geração de números aleatórios consistente
    conjunto_modelos = {}
    
    # Cria 5 modelos com parâmetros aleatórios
    for i in range(6):
        modelo = {
            "n_modelo": i,
            "taxa_mutacao": random.randint(5, 30),
            "taxa_crossover": random.randint(1, 30),
            "geracoes": random.randint(700, 1800),
            "populacao": random.randint(200, 600)
        }
        conjunto_modelos[i] = modelo

    return conjunto_modelos

if __name__ == "__main__":
    d_modelos = modelos()

    # Para cada modelo, cria um arquivo de resultado
    for i in range(1,5):

        with open(f"resultado_genetico_modelo_{i}.txt", "w") as arq:
            arq.write(f"Resultados do Algoritmo Genetico aplicado ao TSP Berlin52 - Modelo {i}:\n")
            arq.write("Parametros:\n")
            
            # Formata os parâmetros de cada modelo
            for chave, valor in d_modelos[i].items():
                arq.write(f"{chave}: {valor}\n")
            
            arq.write("\n")
        tempo = 0
        for j in range(1, 31):
            tempo, menor = main_genetico(j, d_modelos[i], f"resultado_genetico_modelo_{i}.txt",tempo)
        tempo = tempo/30
        menor = menor/30
        with open(f"resultado_genetico_modelo_{i}.txt", "a") as arq:
            arq.write("Tempo medio da amostra: " + str(tempo))
            arq.write("distancia media da amostra: " + str(menor))