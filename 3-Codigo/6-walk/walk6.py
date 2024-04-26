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

def simple_hash(value, alpha):
    return value % alpha

def SummaryGraph(A, alpha):
    n = len(A)
    C = np.zeros((alpha, alpha))
    
    for i in range(n):
        hash_i = simple_hash(i, alpha)
        for j in range(n):
            if A[i][j] == 1:
                hash_j = simple_hash(j, alpha)
                C[hash_i][hash_j] += 1
                C[hash_j][hash_i] = C[hash_i][hash_j]
    
    return C

def EstimateWalks(A, alpha, beta):
    n = len(A)
    cwMin = np.zeros(n)
    
    for i in range(beta):
        cw_prime_i = np.zeros(n)
        Ci = SummaryGraph(A, alpha)
        print(Ci)
        
        for v in range(n):
            dX_v = np.sum(A[v])  # Grau do vértice v no grafo resumido H
            C3_sum = np.sum(np.power(Ci[v], 3))  # Soma dos elementos da terceira potência de Ci[v]
            C2_sum = np.sum(np.power(Ci[v], 2))  # Soma dos elementos da segunda potência de Ci[v]
            
            C6_ii = np.power(C3_sum, 2)  # C6(i,i)
            C4_ii = np.power(C2_sum, 2)  # C4(i,i)
            
            D6_i = np.sum(np.power(np.sum(Ci, axis=1), 6))  # Soma dos graus elevados à sexta potência
            D4_i = np.sum(np.power(np.sum(Ci, axis=1), 4))  # Soma dos graus elevados à quarta potência
            
            cw_prime_i[v] = (6 * C6_ii * np.power(dX_v, 6) / D6_i - 6 * dX_v * C4_ii * np.power(dX_v, 4) / D4_i)
        
        cwMin_i = np.zeros(n)
        for j in range(n):
            cwMin_i[j] = min(cw_prime_i)
        
        if i == 0:
            cwMin = np.copy(cwMin_i)
        else:
            cwMin = np.minimum(cwMin, cwMin_i)
    
    return cwMin


def GreedyNodeImmunization(A, k, alpha, beta):
    n = len(A)
    S = set()
    W2_score = np.zeros(n)
    
    W = EstimateWalks(A, alpha, beta)
    print(W)
    gamma = np.max(W)
    
    for i in range(n):
        W2_score[i] = gamma * W[i] ** 2
    
    for i in range(k):
        aS = np.sum(A[:, list(S)] * W[list(S)], axis=1)
        
        for j in range(n):
            if j not in S:
                Score_j = W2_score[j] - 2 * aS[j] * W[j]
            else:
                Score_j = -1
        
        maxNode = np.argmax(Score_j)
        S.add(maxNode)
    
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
    parser.add_argument("alpha", type=int, help="Parameter alpha")
    parser.add_argument("beta", type=int, help="Parameter beta")
    args = parser.parse_args()

    # Chamada do algoritmo
    A, node_map, G = read_dot_file(args.file_path)
    nodes = GreedyNodeImmunization(A, args.k, args.alpha, args.beta)
    selected_nodes = [list(node_map.keys())[list(node_map.values()).index(node)] for node in nodes]
    drop = eigendrop(G, selected_nodes)

    # Retorno da resposta
    print("Nodos a serem imunizados:", selected_nodes)
    print("Eigendrop: ", drop)
