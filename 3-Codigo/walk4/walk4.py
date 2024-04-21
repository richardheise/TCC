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
import networkx as nx
import argparse

# /***********************************************************************/
# / Algoritmo COMPUTE-SCORE (https://doi.org/10.48550/arXiv.1711.00791)
# /***********************************************************************/

def compute_score(G):
    n = len(G.nodes())
    deg = np.zeros(n)
    codeg_sum = np.zeros(n)
    score = np.zeros(n)
    
    # Calcula o grau de cada vértice
    degrees = dict(G.degree())
    for node, degree in degrees.items():
        deg[node] = degree
    
    # Calcula a soma dos codeg
    for node in G.nodes():
        for neighbor in G.neighbors(node):
            codeg_sum[neighbor] += deg[node] - 1
    
    # Calcula o score de cada vértice
    for node in G.nodes():
        score[node] = 2 * deg[node] ** 2 + 4 * codeg_sum[node] ** 2
    
    return score

# /***********************************************************************/
# / Algoritmo UPDATE-SCORE (https://doi.org/10.48550/arXiv.1711.00791)
# /***********************************************************************/

def update_score(G, score, node, visited):
    deg = dict(G.degree())
    codeg_sum = np.zeros(len(G.nodes()))
    
    # Marca o nó como visitado
    visited[node] = True
    
    # Reduz o grau e a soma dos cograus dos vizinhos do nó
    for neighbor in G.neighbors(node):
        if not visited[neighbor]:
            deg[neighbor] -= 1
            codeg_sum[neighbor] -= (deg[node] - 1)
            for neighbor_of_neighbor in G.neighbors(neighbor):
                codeg_sum[neighbor_of_neighbor] -= 1
    
    # Zera o grau e a soma dos cograus do nó
    deg[node] = 0
    codeg_sum[node] = 0
    score[node] = 0

    # Atualiza o score dos vizinhos do nó
    for neighbor in G.neighbors(node):
        if not visited[neighbor]:
            score[neighbor] = 2 * deg[neighbor] ** 2 + 4 * codeg_sum[neighbor] ** 2
            for neighbor_of_neighbor in G.neighbors(neighbor):
                score[neighbor_of_neighbor] = 2 * deg[neighbor_of_neighbor] ** 2 + 4 * codeg_sum[neighbor_of_neighbor] ** 2
    
    return score


# /***********************************************************************/
# / Algoritmo Walk4 (https://doi.org/10.48550/arXiv.1711.00791)
# /***********************************************************************/

def Walk4(adj_matrix, k):
    S = set()
    G = nx.Graph(adj_matrix)  # Criar um grafo a partir da matriz de adjacência
    score = compute_score(G)
    visited = {node: False for node in G.nodes()}  # Inicializa todos os nodos como não visitados
    
    while len(S) < k:
        # Encontra o índice do nó com o maior score que ainda não está em S
        max_score_node = max((node for node in G.nodes() if not visited[node]), key=lambda node: score[node])
        
        # Adiciona o nó selecionado ao conjunto S
        S.add(max_score_node)
        
        # Atualiza os escores com base no nó selecionado
        score = update_score(G, score, max_score_node, visited)
        
    return S

# /***********************************************************************/
# / Função que calcula eigendrop (autoqueda)
# /***********************************************************************/

def eigendrop(G, S):
    # Matriz de adjacência do grafo original
    A_original = nx.adjacency_matrix(G).toarray()

    # Maior autovalor do grafo original
    largest_eigenvalue_original = np.max(np.linalg.eigvals(A_original))
    
    # Criar um novo grafo removendo os vértices em S
    G_removed = G.copy()
    G_removed.remove_nodes_from(S)
    
    # Matriz de adjacência do novo grafo
    A_removed = nx.adjacency_matrix(G_removed).toarray()

    # Maior autovalor do novo grafo
    largest_eigenvalue_removed = np.max(np.linalg.eigvals(A_removed))
    
    # Calcula o eigendrop
    eigendrop_value = largest_eigenvalue_original - largest_eigenvalue_removed

    return eigendrop_value

# /***********************************************************************/
# / Função para ler arquivo .dot e retornar a matriz de adjacência
# /***********************************************************************/

def read_dot_file(file_path):
    print(f"Lendo arquivo .dot em {file_path}...")
    G = nx.drawing.nx_pydot.read_dot(file_path)
    nodes = list(G.nodes)
    node_map = {node: i for i, node in enumerate(nodes)}
    adj_matrix = nx.adjacency_matrix(G, nodelist=nodes).toarray()
    
    return adj_matrix, node_map, G

# /***********************************************************************/
# / Main
# /***********************************************************************/

if __name__ == "__main__":

    # Parsing de argumentos da entrada padrão
    parser = argparse.ArgumentParser(description="NetShield+ algorithm implementation")
    parser.add_argument("file_path", type=str, help="Path to the .dot file")
    parser.add_argument("k", type=int, help="Number of nodes to select")
    args = parser.parse_args()

    # Chamada do algoritmo
    A, node_map, G = read_dot_file(args.file_path)
    nodes = Walk4(A, args.k)
    selected_nodes = [list(node_map.keys())[list(node_map.values()).index(node)] for node in nodes]
    drop = eigendrop(G, selected_nodes)

    # Retorno da resposta
    print("Nodos a serem imunizados:", selected_nodes)
    print("Eigendrop: ", drop)

