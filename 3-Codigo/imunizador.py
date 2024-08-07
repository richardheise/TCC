#!/bin/python3

# /***********************************************************************/
#
# Autor: Richard Fernando Heise Ferreira
# GRR: 20191053
# Data: 04/2024
# Instituição: Universidade Federal do Paraná
# Curso: Ciência da Computação
# Motivo: Trabalho de Conclusão de Curso
#
# /***********************************************************************/


# Imports
from collections import defaultdict
from math import floor, ceil
import numpy as np
import scipy.sparse
import scipy.linalg
import networkx as nx
import argparse
import itertools
import time
import inbox
import csv
import os

##################### ALGORITMOS #########################################
#-->

# /***********************************************************************/
# / Algoritmo COMPUTE-SCORE (https://doi.org/10.48550/arXiv.1711.00791)
# /***********************************************************************/
def compute_score(G, degrees, codeg_sum, score):
    
    # Calcula a soma dos codeg
    for node in G.nodes():
        for neighbor in G.neighbors(node):
            codeg_sum[neighbor] += degrees[node] - 1
    
    # Calcula o score de cada vértice
    for node in G.nodes():
        score[node] = 2 * degrees[node] ** 2 + 4 * codeg_sum[node] ** 2

    return score

# /***********************************************************************/
# / Algoritmo UPDATE-SCORE (https://doi.org/10.48550/arXiv.1711.00791)
# /***********************************************************************/
def update_score(G, node, degrees, codeg_sum, score):
    
    # Reduz o grau e a soma dos cograus dos vizinhos do nodo
    for neighbor in G.neighbors(node):
        degrees[neighbor] -= 1
        codeg_sum[neighbor] -= (degrees[node] - 1)
        for neighbor_of_neighbor in G.neighbors(neighbor):
            codeg_sum[neighbor_of_neighbor] -= 1

    # Zera o grau e a soma dos cograus do nodo
    degrees[node] = 0
    codeg_sum[node] = 0
    score[node] = 0
    neighbors = list(G.neighbors(node))
    G.remove_node(node)

    # Atualiza o score dos vizinhos do nodo
    for neighbor in neighbors:
        score[neighbor] = 2 * degrees[neighbor] ** 2 + 4 * codeg_sum[neighbor] ** 2
        for neighbor_of_neighbor in G.neighbors(neighbor):
            score[neighbor_of_neighbor] = 2 * degrees[neighbor_of_neighbor] ** 2 + 4 * codeg_sum[neighbor_of_neighbor] ** 2

    return score

# /***********************************************************************/
# / Algoritmo Walk4 (https://doi.org/10.48550/arXiv.1711.00791)
# /***********************************************************************/
def Walk4(G, k):

    S = set()
    degrees = dict(G.degree())
    codeg_sum = {node: 0 for node in G.nodes()}
    score = {node: 0 for node in G.nodes()}

    G_local = G.copy()
    score = compute_score(G_local, degrees, codeg_sum, score)
    
    while len(S) < k:
        # Encontra o índice do nodo com o maior score que ainda não está em S
        max_score_node = max((node for node in G_local.nodes()), key=lambda node: score[node])

        # Adiciona o nodo selecionado ao conjunto S
        S.add(max_score_node)

        # Atualiza os escores com base no nodo selecionado
        score = update_score(G_local, max_score_node, degrees, codeg_sum, score)

    return S

# /***********************************************************************/
# / Algoritmo COMPUTE-SCORE-Aprimorado
# /***********************************************************************/
def compute_score_enhanced(G, degrees, codeg_sum, score):
    
    # Calcula a soma dos codeg
    for node in G.nodes():
        for neighbor in G.neighbors(node):
            codeg_sum[neighbor] += degrees[node] - 1
    
    # Calcula o score de cada vértice
    for node in G.nodes():
        if degrees[node] != 1:
            score[node] = 2 * degrees[node] ** 2 + 4 * codeg_sum[node] ** 2

    return score

# /***********************************************************************/
# / Algoritmo UPDATE-SCORE-Aprimorado
# /***********************************************************************/
def update_score_enhanced(G, node, degrees, codeg_sum, score):
    
    # Reduz o grau e a soma dos cograus dos vizinhos do nodo
    for neighbor in G.neighbors(node):
        degrees[neighbor] -= 1
        codeg_sum[neighbor] -= (degrees[node] - 1)
        for neighbor_of_neighbor in G.neighbors(neighbor):
            codeg_sum[neighbor_of_neighbor] -= 1

    # Zera o grau e a soma dos cograus do nodo
    degrees[node] = 0
    codeg_sum[node] = 0
    score[node] = 0
    neighbors = list(G.neighbors(node))
    G.remove_node(node)

    # Atualiza o score dos vizinhos do nodo
    for neighbor in neighbors:
        if (degrees[neighbor] == 1):
            score[neighbor] = 0
        else:
            score[neighbor] = 2 * degrees[neighbor] ** 2 + 4 * codeg_sum[neighbor] ** 2

        for neighbor_of_neighbor in G.neighbors(neighbor):
            if (degrees[neighbor_of_neighbor] == 1):
                score[neighbor_of_neighbor] = 0
            else:
                score[neighbor_of_neighbor] = 2 * degrees[neighbor_of_neighbor] ** 2 + 4 * codeg_sum[neighbor_of_neighbor] ** 2

    return score

# /***********************************************************************/
# / Algoritmo Walk4-Aprimorado
# /***********************************************************************/
def Walk4_enhanced(G, k):

    S = set()
    score = {node: 0 for node in G.nodes()}
    degrees = dict(G.degree())
    codeg_sum = {node: 0 for node in G.nodes()}

    G_local = G.copy()
    score = compute_score_enhanced(G_local, degrees, codeg_sum, score)
    
    while len(S) < k:
        # Encontra o índice do nodo com o maior score que ainda não está em S
        max_score_node = max((node for node in G_local.nodes()), key=lambda node: score[node])

        # Adiciona o nodo selecionado ao conjunto S
        S.add(max_score_node)

        # Atualiza os escores com base no nodo selecionado
        score = update_score_enhanced(G_local, max_score_node, degrees, codeg_sum, score)

    return S

# /***********************************************************************/
# / Algoritmo NETSHIELD (DOI: 10.1109/TKDE.2015.2465378)
# /***********************************************************************/
def net_shield(A, k):
    n = A.shape[0]
    
    # Passo 1: Calculando o primeiro (maior) autovalor e autovetor correspondente
    eigenvalues, eigenvectors = np.linalg.eig(A)
    max_eigenvalue_idx = np.argmax(eigenvalues)
    eigenvalues = eigenvalues[max_eigenvalue_idx].real
    eigenvectors = eigenvectors[:, max_eigenvalue_idx].real
    
    # Passo 2: Inicializando o conjunto S
    S = set()
    
    # Passo 3: Calculando shield-value para cada nodo
    v = np.zeros(n)
    for j in range(n):
        v[j] = (2 * eigenvalues - A[j, j]) * eigenvectors[j] ** 2
    
    # Passo 6-17: Selecionando os nós para S iterativamente
    for _ in range(k):
        B = A[:, list(S)] if S else np.zeros((n, 0))
        b = np.dot(B, eigenvectors[list(S)])
        
        score = np.zeros(n)
        for j in range(n):
            if j in S:
                score[j] = -1
            else:
                score[j] = v[j] - 2 * b[j] * eigenvectors[j]
        
        i = np.argmax(score)
        S.add(i)
    
    return S

# /***********************************************************************/
# / Algoritmo NETSHIELD+ (DOI: 10.1109/TKDE.2015.2465378)
# /***********************************************************************/
def netshield_plus(G, k, b):

    A = nx.adjacency_matrix(G).toarray()
    n = A.shape[0]
    t = b * k // n

    S = set()

    for _ in range(t):
        S_prime = net_shield(A, b)
        S.update(S_prime)
        A = np.delete(A, list(S_prime), axis=0)
        A = np.delete(A, list(S_prime), axis=1)

    if k > t * b:
        S_prime = net_shield(A, k - t * b)
        S.update(S_prime)
    
    immunized = [list(G.nodes())[i] for i in S]
    
    return immunized

# /***********************************************************************/
# / Algoritmo Força-Bruta
# /***********************************************************************/
def brute_force(G, k):

    print(f"Rodando brute force em {len(G.nodes())} vértices e {len(G.edges)} arestas para {k} recursos...")
    start_time = time.perf_counter()
     
    best_subset = None
    best_drop = float('-inf')

    # Calcula o eigendrop para todos os subconjuntos de tamanho k
    for subset in itertools.combinations(G.nodes(), k):
        drop = eigendrop(G, subset)
        if drop > best_drop:
            best_drop = drop
            best_subset = subset

    end_time = time.perf_counter()
    exec_time = end_time - start_time
    minutes, seconds = divmod(exec_time, 60)
    print(f"Rodou em {int(minutes)}:{seconds:02} minuto(s).")

    return best_subset

#<--

##################### UTILITÁRIOS #########################################
#-->

# /***********************************************************************/
# / Calcula eigendrop
# /***********************************************************************/
def eigendrop(G, S):

    # Matriz de adjacência do grafo original
    largest_eigenvalue_original = max(nx.adjacency_spectrum(G))
    
    # Criar um novo grafo removendo os vértices em S
    G_removed = G.copy()
    G_removed.remove_nodes_from(S)

    # Maior autovalor do novo grafo
    largest_eigenvalue_removed = max(nx.adjacency_spectrum(G_removed))
    
    # Calcula o eigendrop
    eigendrop = largest_eigenvalue_original - largest_eigenvalue_removed

    return eigendrop

# /***********************************************************************/
# / Seleciona algoritmo a ser usado
# /***********************************************************************/
def select_algorithm(G, id):

    k = int(input(f"Quantos recursos temos?: \n"))

    if (k >= len(G.nodes())-1):
        print("Temos mais recursos que nodos, logo, imunize todo mundo!")
        exit(0)

    to_immunize = ()
    
    match id:
        
        case 1:
            print(f"Rodando Brute Force em {len(G.nodes())} vértices e {len(G.edges())} arestas para {k} recursos...")
            start_time = time.perf_counter()

            to_immunize = brute_force(G, k)

            end_time = time.perf_counter()
            exec_time = end_time - start_time
            minutes, seconds = divmod(exec_time, 60)
            print(f"Brute Force rodou em {int(minutes)}:{seconds:.2f} minuto(s).")

        case 2:
            b = int(input(f"Escolha o valor de b (inteiro) do NetShield+: \n"))
            print(f"Rodando NetShield+ em {len(G.nodes())} vértices e {len(G.edges())} arestas para {k} recursos...")
            start_time = time.perf_counter()

            to_immunize = netshield_plus(G, k, b)

            end_time = time.perf_counter()
            exec_time = end_time - start_time
            minutes, seconds = divmod(exec_time, 60)
            print(f"NetShield+ rodou em {int(minutes)}:{seconds:.2f} minuto(s).")

        case 3:
            print(f"Rodando Walk4 em {len(G.nodes())} vértices e {len(G.edges())} arestas para {k} recursos...")
            start_time = time.perf_counter()

            to_immunize = Walk4(G, k)

            end_time = time.perf_counter()
            exec_time = end_time - start_time
            minutes, seconds = divmod(exec_time, 60)
            print(f"Walk4 rodou em {int(minutes)}:{seconds:.2f} minuto(s).")

        case 4:
            print(f"Rodando Walk4 Enhanced em {len(G.nodes())} vértices e {len(G.edges())} arestas para {k} recursos......")
            start_time = time.perf_counter()

            to_immunize = Walk4_enhanced(G, k)

            end_time = time.perf_counter()
            exec_time = end_time - start_time
            minutes, seconds = divmod(exec_time, 60)
            print(f"Walk4 Enhanced rodou em {int(minutes)}:{seconds:.2f} minuto(s).")

        case 5:
            print(f"Rodando XNB-Centrality em {len(G.nodes())} vértices e {len(G.edges())} arestas para {k} recursos...")
            start_time = time.perf_counter()

            to_immunize, _ = inbox.immunize(G, k, strategy='xnb')

            end_time = time.perf_counter()
            exec_time = end_time - start_time
            minutes, seconds = divmod(exec_time, 60)
            print(f"XNB-Centrality rodou em {int(minutes)}:{seconds:.2f} minuto(s).")

        case _:
            print("Valor inválido")

    return to_immunize, eigendrop(G, to_immunize)


# /***********************************************************************/
# / Lê o .dot
# /***********************************************************************/
def read_dot_file(file_path):
    print(f"Lendo arquivo .dot em {file_path}...")
    G = nx.drawing.nx_pydot.read_dot(file_path)

    return nx.Graph(G)

# /***********************************************************************/
# / Gera os resultados dos testes
# /***********************************************************************/
def results(G, input_file_name):

    k = ceil(len(G.nodes()) / 4)
    ks = [floor(k / 5), floor(k / 4), floor(k / 3), floor(k / 2), k]

    # Remove duplicatas e zeros
    ks = sorted(list(set(filter(lambda x: x != 0, ks))))

    # Define o nome do arquivo CSV baseado no nome do arquivo de entrada
    output_file_name = f'results_{os.path.splitext(input_file_name)[0]}.csv'

    # Abre o arquivo CSV para escrita
    with open(output_file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Escreve o cabeçalho
        writer.writerow(['algoritmo', 'k', 'time', 'eigendrop'])

        for k in ks:
            print("k:", k)
            
            # Netshield
            b = ceil(k / 10)

            if b > 100:
                b = 100
            start_time = time.perf_counter()
            to_immunize = netshield_plus(G, k, b)
            end_time = time.perf_counter()
            exec_time = end_time - start_time
            eigendrop_final = eigendrop(G, to_immunize)
            print(f"netshield - k: {k}, time: {exec_time}, eigendrop: {eigendrop_final.real}")
            writer.writerow(['netshield', k, exec_time, round(eigendrop_final.real, 8)])
        
            # Walk4
            start_time = time.perf_counter()
            to_immunize = Walk4(G, k)
            end_time = time.perf_counter()
            exec_time = end_time - start_time
            eigendrop_final = eigendrop(G, to_immunize)
            print(f"walk4 - k: {k}, time: {exec_time}, eigendrop: {eigendrop_final.real}")
            writer.writerow(['walk4', k, exec_time, round(eigendrop_final.real, 8)])

            # Walk4 Aprimorado
            start_time = time.perf_counter()
            to_immunize = Walk4_enhanced(G, k)
            end_time = time.perf_counter()
            exec_time = end_time - start_time
            eigendrop_final = eigendrop(G, to_immunize)
            print(f"walk4-aprimorado - k: {k}, time: {exec_time}, eigendrop: {eigendrop_final.real}")
            writer.writerow(['walk4-aprimorado', k, exec_time, round(eigendrop_final.real, 8)])

            # XNB
            start_time = time.perf_counter()
            to_immunize, _ = inbox.immunize(G, k, strategy='xnb')
            end_time = time.perf_counter()
            exec_time = end_time - start_time
            eigendrop_final = eigendrop(G, to_immunize)
            print(f"xnb - k: {k}, time: {exec_time}, eigendrop: {eigendrop_final.real}")
            writer.writerow(['xnb', k, exec_time, round(eigendrop_final.real, 8)])

            print("\n")

#<--

##################### MAIN #########################################
#-->
if __name__ == "__main__":

    # Parsing de argumentos da entrada padrão
    parser = argparse.ArgumentParser(description="Imunizador de Nodos de um grafo")
    parser.add_argument("file_path", type=str, help="Caminho do arquivo .dot ou pasta (-t)")
    parser.add_argument("-t", action="store_true", help="Executar testes em todos os arquivos na pasta")
    args = parser.parse_args()

    if args.t:
        # Se o argumento -t foi fornecido, processar todos os arquivos .dot na pasta
        folder_path = args.file_path
        for filename in os.listdir(folder_path):
            if filename.endswith(".dot"):
                file_path = os.path.join(folder_path, filename)
                print(f"Processando arquivo: {file_path}")
                G = read_dot_file(file_path)
                results(G, filename)
    else:
        # Chamada do algoritmo
        G = read_dot_file(args.file_path)

        algorithm_id = int(input("""
Escolha qual algoritmo deseja usar:
1 --> BruteForce
2 --> Netshield+
3 --> Walk-4
4 --> Walk-4-Enhanced
5 --> XNB-Centrality
6 --> Testes (b = k/10)
"""))

        if (algorithm_id == 6):
            results(G)
            exit(0)

        immunized, max_eigendrop = select_algorithm(G, algorithm_id)

        max_eigendrop = round(max_eigendrop.real, 8)

        G_final = G.copy()
        G_final.remove_nodes_from(immunized)

        # Retorno da resposta
        print("Nodos a serem imunizados:", list(immunized))
        print(f"Maior autovalor inicial: {round(max(nx.adjacency_spectrum(G)).real, 8):.8f}")
        print(f"Maior autovalor final: {round(max(nx.adjacency_spectrum(G_final)).real, 8):.8f}")
        print(f"Autoqueda: {max_eigendrop:.8f}")

#<--
