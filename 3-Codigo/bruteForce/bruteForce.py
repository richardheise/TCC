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

def bruteForce(A, k, debug=False):
    best_subset = None
    best_drop = float('-inf')
    n = len(A)

    # Gerar todos os subconjuntos de tamanho k de vértices
    subsets = itertools.combinations(range(n), k)

    # Calcula o eigendrop para todos os subconjuntos
    eigendrops = [(subset, eigendrop(A, subset)) for subset in subsets]

    # Encontra o subconjunto com o maior eigendrop
    best_subset, best_drop = max(eigendrops, key=lambda x: x[1])

    return best_subset, best_drop

def eigendrop(A, S):
    # Matriz de adjacência do grafo original
    largest_eigenvalue_original = np.max(np.linalg.eigvals(A))
    
    # Criar um novo grafo removendo os vértices em S
    A_removed = np.delete(np.delete(A, S, axis=0), S, axis=1)

    # Maior autovalor do novo grafo
    largest_eigenvalue_removed = np.max(np.linalg.eigvals(A_removed))
    
    # Calcula o eigendrop
    eigendrop_value = largest_eigenvalue_original - largest_eigenvalue_removed
    return eigendrop_value

def read_dot_file(file_path):
    print(f"Lendo arquivo .dot em {file_path}...")
    G = nx.drawing.nx_pydot.read_dot(file_path)
    nodes = list(G.nodes)
    node_map = {node: i for i, node in enumerate(nodes)}
    adj_matrix = nx.adjacency_matrix(G).toarray()

    return G, adj_matrix, node_map

if __name__ == "__main__":
    # Parsing de argumentos da entrada padrão
    parser = argparse.ArgumentParser(description="NetShield+ algorithm implementation")
    parser.add_argument("file_path", type=str, help="Path to the .dot file")
    parser.add_argument("k", type=int, help="Number of nodes to select")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug prints")
    args = parser.parse_args()

    # Chamada do algoritmo
    G, A, node_map = read_dot_file(args.file_path)
    immunized, best_drop = bruteForce(A, args.k, args.debug)

    print(max(nx.adjacency_spectrum(G)))
    print(max(nx.adjacency_spectrum(G.remove_nodes_from(immunized))))

    idxToName = [list(node_map.keys())[list(node_map.values()).index(i)] for i in immunized]
    eigendrop_rounded = round(best_drop.real, 8)

    # Retorno da resposta
    print("Nodos a serem imunizados:", idxToName)
    print(f"Eigendrop: {eigendrop_rounded:.8f}")
