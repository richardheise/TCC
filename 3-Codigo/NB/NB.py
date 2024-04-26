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
import inbox

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
    
    return G

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
    G = read_dot_file(args.file_path)
    selected_nodes = inbox.immunize(G, args.k, strategy='xnb')

    # drop = eigendrop(G, selected_nodes)

    # Retorno da resposta
    print("Nodos a serem imunizados:", selected_nodes)
    # print("Eigendrop: ", drop)

