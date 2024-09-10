#devido a complexidade do problema berlin52 o mapa utilizado foi reduzido apenas aos primeiros 8 pontos do original sendo armazenado no arquivo berlin8.tsp
import itertools
import math

def ler_arquivo_tsp(arquivo):
    with open("berlin8.tsp", 'r') as file:
        linhas = file.readlines()
        
    pontos = {}
    ler = False
    for linha in linhas:
        if linha.startswith("NODE_COORD_SECTION"):
            ler = True
            continue
        if ler:
            if linha.strip() == "EOF":
                break
            partes = linha.split()
            ponto_id = int(partes[0])
            x = float(partes[1])
            y = float(partes[2])
            pontos[ponto_id] = (x, y)
    
    return pontos

def dist_euclideana(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

def dist_total(rota, pontos):
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += dist_euclideana(pontos[rota[i]], pontos[rota[i+1]])
    distancia_total += dist_euclideana(pontos[rota[-1]], pontos[rota[0]])
    return distancia_total

def forca_bruta_tsp(pontos):
    cidades = list(pontos.keys())
    melhor_rota = None
    min_distancia = float('inf')
    
    for permutation in itertools.permutations(cidades[1:]):
        rota_atual = [cidades[0]] + list(permutation)
        dist_atual = dist_total(rota_atual, pontos)
        
        if dist_atual < min_distancia:
            min_distancia = dist_atual
            melhor_rota = rota_atual
    
    return melhor_rota, min_distancia

arquivo = 'berlin8.tsp'
pontos = ler_arquivo_tsp(arquivo)
melhor_rota, min_distancia = forca_bruta_tsp(pontos)

print("Melhor rota encontrada:", melhor_rota)
print("Menor distância:", min_distancia)