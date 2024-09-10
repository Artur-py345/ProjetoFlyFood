import random

def achando_posiçoes(nome):

    """ Cria um dicionário de listas com as coordenadas de cada ponto
    Exemplo: 1:[0,10] """
    
   # Linhas abaixo abrem o arquivo transfomando cada linha em um elemento de uma lista,
   # excluindo o cabeçalho.

    arq = open(nome,"r+")
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

def caminho_entre(pos_1, pos_2, novo_ponto):

    """Função que descobre a distância entre dois pontos"""

    x_1, y_1 = pos_1[0], pos_1[1]
    x_2, y_2 = pos_2[0], pos_2[1]

    diferença_x = abs(x_1 - x_2)
    diferença_y = abs(y_1 - y_2)

    distancia = (diferença_x**2) + (diferença_y**2)
    distancia = distancia**(1/2)
    
    return distancia, novo_ponto

def comparando(distancia ,nova_distancia, ponto, novo_ponto):
    """ Compara o novo ponto com o anterior e retorna o menor """

    if nova_distancia < distancia:
        return nova_distancia, novo_ponto
    
    return distancia, ponto

def busca_proximo(atual, posiçoes, n_pontos, caminho, lista):

    """ Função que previne que o mesmo ponto seja repitido e descobre um novo """
    distancia = float("inf")
    ponto = float("inf")
    #
    for ponto_analisado in lista:

        if ponto_analisado in caminho:
            continue
        else:
            nova_distancia, novo_ponto = caminho_entre(posiçoes[atual], posiçoes[ponto_analisado], ponto_analisado)
            menor_distancia, menor_ponto = comparando(distancia, nova_distancia, ponto, novo_ponto)
            distancia = menor_distancia
            ponto = menor_ponto

    return ponto, distancia

def descobrindo_caminho(atual, n_pontos, posiçoes,lista):

    """Função que recebe o ponto de partida e começa a somar a distância a partir dele,
    construindo o caminho"""
    
    caminho = [None] * (n_pontos + 1)
    distancia_total = 0
    caminho[0] = atual
    caminho[len(caminho)-1] = atual
    rodadas = 1
    #laço que termina após a penultima posição da lista 'caminho' ser preenchida
    
    while caminho[n_pontos-1] == None:

        proximo_ponto, distancia = busca_proximo(atual, posiçoes, n_pontos, caminho,lista)
        distancia_total += distancia
        caminho[rodadas] = proximo_ponto
        atual = proximo_ponto
        rodadas +=1
    
    ultima_distancia, ultimo_ponto = caminho_entre(posiçoes[caminho[len(caminho)- 2]], posiçoes[caminho[len(caminho)- 1]], caminho[len(caminho)- 1] )
    distancia_total += ultima_distancia

    return caminho, distancia_total

def guardando_guloso(caminho, distancia):
    
    with open("resultado_guloso.txt", "a") as arq:
        
        for i in range(len(caminho)):
            arq.write(str(caminho[i]))
            if i < len(caminho) - 1:
                arq.write("/")
        
        arq.write("\n")
        
        arq.write(str(distancia))
        arq.write("\n")

def main(inicial, pontos, posiçoes, n_pontos):

    caminho, distancia = descobrindo_caminho(inicial, n_pontos, posiçoes,pontos)
    return caminho, distancia

if __name__ == "__main__":
    for i in range(1,53):
        lista = [i for i in range(1,53)]
        posiçoes, n_pontos = achando_posiçoes("berlin52.tsp")
        caminho, distancia = main(i, lista, posiçoes, n_pontos)
        guardando_guloso(caminho, distancia)