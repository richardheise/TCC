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
import networkx as nx
import argparse
from scipy.sparse.linalg import eigs

def largest_connected_component(G):
    # Encontra o maior componente conectado
    lcc_nodes = max(nx.connected_components(G), key=len)
    return G.subgraph(lcc_nodes).copy()

def fiedler_vector(G):
    # Calcula o vetor de Fiedler usando o segundo menor autovalor
    n = len(G)
    L = nx.laplacian_matrix(G).astype(float)
    _, eig_vecs = eigs(L, k=2, which='SM')
    fiedler_vec = eig_vecs[:, 1].real
    return fiedler_vec

def likelihood_partition(G, fiedler_vec):
    # Calcula a probabilidade de cada partição
    sorted_nodes = sorted(G.nodes(), key=lambda x: fiedler_vec[list(G.nodes()).index(x)])
    n = len(sorted_nodes)
    likelihood = []
    for i in range(1, n):
        partition = set(sorted_nodes[:i])
        cut_size = nx.cut_size(G, partition)
        likelihood.append(cut_size / (i * (n - i)))
    return likelihood

def immunize_nodes(G, k, partition):
    # Imuniza os nós de acordo com a partição
    immunized_nodes = []
    for node, part in partition.items():
        if part == 1 and k > 0:
            immunized_nodes.append(node)
            k -= 1
    return immunized_nodes, k

def separate_groups(G, partition):
    # Encontra os nós que conectam os dois grupos
    connecting_nodes = set()
    for u, v in G.edges():
        if partition[u] != partition[v]:
            connecting_nodes.add(u)
            connecting_nodes.add(v)
    
    # Calcula o número de arestas de cada nó conectando para o outro grupo
    num_edges_to_other_group = {node: 0 for node in connecting_nodes}
    for node in connecting_nodes:
        for neighbor in G.neighbors(node):
            if partition[node] != partition[neighbor]:
                num_edges_to_other_group[node] += 1
    
    # Separa os dois grupos removendo os nós conectores
    while len(set(partition.values())) > 1:
        # Encontra o nó com o máximo de arestas para o outro grupo
        max_edges_node = max(num_edges_to_other_group, key=num_edges_to_other_group.get)
        
        # Remove o nó com o máximo de arestas para o outro grupo
        partition.pop(max_edges_node)
        G.remove_node(max_edges_node)
        
        # Atualiza o número de arestas para o outro grupo dos nós restantes
        for neighbor in G.neighbors(max_edges_node):
            if partition[neighbor] != partition[max_edges_node]:
                num_edges_to_other_group[neighbor] -= 1
    
    # Retorna os dois grupos separados
    group_1 = {node for node, part in partition.items() if part == 0}
    group_2 = {node for node, part in partition.items() if part == 1}
    return group_1, group_2

def immunization_algorithm(G, k):
    immunized_nodes = []
    while k > 0:
        # Passo 1: Determinar o maior componente conectado da rede
        lcc = largest_connected_component(G)
        
        # Passo 2: Calcular o vetor de Fiedler para o LCC
        fiedler_vec = fiedler_vector(lcc)
        
        # Passo 3: Calcular a probabilidade de todas as partições
        likelihood = likelihood_partition(lcc, fiedler_vec)
        
        # Passo 4: Escolher a partição com a maior probabilidade que requer menos de k nós para separar
        max_likelihood_idx = np.argmax(likelihood)
        lcc_nodes = list(lcc.nodes())
        max_likelihood_node = lcc_nodes[max_likelihood_idx]
        partition = {node: 0 if fiedler_vec[list(G.nodes()).index(node)] < fiedler_vec[list(G.nodes()).index(max_likelihood_node)] else 1 for node in lcc_nodes}


        
        # Passo 5: Imunizar os nós necessários e separar os dois grupos
        immunized, k = immunize_nodes(G, k, partition)
        immunized_nodes.extend(immunized)
        
        # Passo 6: Atualizar o valor de k
        k = max(0, k)
    
    return immunized_nodes

# Função para ler arquivo .dot e retornar o grafo
def read_dot_file(file_path):
    print(f"Lendo arquivo .dot em {file_path}...")
    G = nx.drawing.nx_pydot.read_dot(file_path)
    return G

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Immunization algorithm implementation")
    parser.add_argument("file_path", type=str, help="Path to the .dot file")
    parser.add_argument("k", type=int, help="Number of immunization resources")
    args = parser.parse_args()

    G = read_dot_file(args.file_path)
    immunized_nodes = immunization_algorithm(G, args.k)
    print("Nós imunizados:", immunized_nodes)
