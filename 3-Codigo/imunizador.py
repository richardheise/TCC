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
import numpy as np
import scipy.sparse
import scipy.linalg
import networkx as nx
import argparse
import itertools
import time

##################### ALGORITMOS #########################################
#-->

# /***********************************************************************/
# / Algoritmo NETSHIELD (DOI: 10.1109/TKDE.2015.2465378)
# /***********************************************************************/
def net_shield(A, k):
    n = A.shape[0]
    
    # Passo 1: Calculando o primeiro (maior) autovalor e autovetor correspondente
    lambda_, u = np.linalg.eig(A)
    max_lambda_idx = np.argmax(lambda_)
    lambda_ = lambda_[max_lambda_idx].real
    u = u[:, max_lambda_idx].real
    
    # Passo 2: Inicializando o conjunto S
    S = set()
    
    # Passo 3: Calculando shield-value para cada nodo
    v = np.zeros(n)
    for j in range(n):
        v[j] = (2 * lambda_ - A[j, j]) * u[j] ** 2
    
    # Passo 6-17: Selecionando os nós para S iterativamente
    for iter in range(k):
        B = A[:, list(S)] if S else np.zeros((n, 0))
        b = np.dot(B, u[list(S)])
        
        score = np.zeros(n)
        for j in range(n):
            if j in S:
                score[j] = -1
            else:
                score[j] = v[j] - 2 * b[j] * u[j]
        
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

    return S, eigendrop(G, S)

# /***********************************************************************/
# / Algoritmo Força-Bruta
# /***********************************************************************/
def brute_force(G, k):
    
    best_subset = None
    best_drop = float('-inf')

    # Gerar todos os subconjuntos de tamanho k de vértices
    subsets = itertools.combinations(G.nodes(), k)

    # Calcula o eigendrop para todos os subconjuntos
    eigendrops = [(subset, eigendrop(G, subset)) for subset in subsets]

    # Encontra o subconjunto com o maior eigendrop
    best_subset, best_drop = max(eigendrops, key=lambda x: x[1])

    return best_subset, best_drop

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

    if (k >= len(G.nodes())):
        print("Temos mais recursos que nodos, logo, imunize todo mundo!")
        return set(G.nodes()), max(nx.adjacency_spectrum(G))
    
    to_immunize = ()
    eigendrop_final = 0
    
    match id:
        case 1:
            print(f"Rodando brute force em {len(G.nodes())} vértices e {len(G.edges)} arestas para {k} recursos...")
            to_immunize, eigendrop_final = brute_force(G, k)
        case 2:
            b = int(input(f"Escolha o valor de b (inteiro) do NetShield+: \n"))
            print(f"Rodando Netshield+ em {len(G.nodes())} vértices e {len(G.edges)} arestas para {k} recursos...")
            to_immunize, eigendrop_final = netshield_plus(G, k, b)
        case 3:
            print("Rodando Walk-4...")
            # Chame a função correspondente ao algoritmo Walk-4 aqui
        case 4:
            print("Rodando Walk-6...")
            # Chame a função correspondente ao algoritmo Walk-6 aqui
        case 5:
            print("Rodando NB-Centrality...")
            # Chame a função correspondente ao algoritmo NB-Centrality aqui
        case _:
            print("Valor inválido")

    return to_immunize, eigendrop_final

# /***********************************************************************/
# / Lê o .dot
# /***********************************************************************/
def read_dot_file(file_path):
    print(f"Lendo arquivo .dot em {file_path}...")
    G = nx.drawing.nx_pydot.read_dot(file_path)

    return G
#<--

##################### MAIN #########################################
#-->
if __name__ == "__main__":

    # Parsing de argumentos da entrada padrão
    parser = argparse.ArgumentParser(description="Imunizador de Nodos de um grafo")
    parser.add_argument("file_path", type=str, help="Caminho do arquivo .dot")
    args = parser.parse_args()

    # Chamada do algoritmo
    G = read_dot_file(args.file_path)

    algorithm_id = int(input("""
Escolha qual algoritmo deseja usar:
1 --> BruteForce
2 --> Netshield+
3 --> Walk-4
4 --> Walk-6
5 --> NB-Centrality
"""))
    
    start_time = time.time()

    immunized, max_eigendrop = select_algorithm(G, algorithm_id)

    end_time = time.time()
    exec_time = end_time - start_time
    minutes, seconds = divmod(exec_time, 60)

    print(f"Rodou em {int(minutes)}:{seconds:02} minuto(s).")

    max_eigendrop = round(max_eigendrop.real, 8)

    # Retorno da resposta
    print("Nodos a serem imunizados:", list(immunized))
    print(f"Eigendrop: {max_eigendrop:.8f}")
#<--