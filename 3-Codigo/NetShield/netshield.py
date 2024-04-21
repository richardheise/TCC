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
# / Algoritmo NETSHIELD (DOI: 10.1109/TKDE.2015.2465378)
# /***********************************************************************/

def net_shield(A, k, debug=False):
    n = A.shape[0]

    if debug:
        print("Número de vértices: ")
        print(n)
        print("Matriz de Adjacência:")
        print(A)
    
    # Passo 1: Calculando o primeiro (maior) autovalor e autovetor correspondente
    lambda_, u = np.linalg.eig(A)
    max_lambda_idx = np.argmax(lambda_)
    lambda_ = lambda_[max_lambda_idx].real
    u = u[:, max_lambda_idx].real
    if debug:
        print("Primeiro autovalor:", lambda_)
        print("Autovetor correspondente:")
        print(u)
    
    # Passo 2: Inicializando o conjunto S
    S = set()
    if debug:
        print("Conjunto S inicializado:", S)
    
    # Passo 3: Calculando shield-value para cada nodo
    v = np.zeros(n)
    for j in range(n):
        v[j] = (2 * lambda_ - A[j, j]) * u[j] ** 2
    if debug:
        print("v(j) para cada j:")
        print(v)
    
    # Passo 6-17: Selecionando os nós para S iterativamente
    for iter in range(k):
        B = A[:, list(S)] if S else np.zeros((n, 0))
        b = np.dot(B, u[list(S)])
        if debug:
            print(f"Iteração {iter+1}: Matriz B:")
            print(B)
            print(f"Iteração {iter+1}: Vetor b:")
            print(b)
        
        score = np.zeros(n)
        for j in range(n):
            if j in S:
                score[j] = -1
            else:
                score[j] = v[j] - 2 * b[j] * u[j]
        if debug:
            print(f"Iteração {iter+1}: Score de cada nó:")
            print(score)
        
        i = np.argmax(score)
        S.add(i)
        if debug:
            print(f"Iteração {iter+1}: Adicionado nó {i} ao conjunto S")
            print(f"Iteração {iter+1}: Conjunto S atualizado:", S)
    
    return S

# /***********************************************************************/
# / Algoritmo NETSHIELD+ (DOI: 10.1109/TKDE.2015.2465378)
# /***********************************************************************/

def netshield_plus(A, k, b, debug=False):
    n = A.shape[0]
    t = b * k // n

    if (debug): 
        print(f"Valor de t: {t}\nvalor de k: {k}\nvalor de n: {n}")

    S = set()

    for _ in range(t):
        S_prime = net_shield(A, b, debug)
        S.update(S_prime)
        A = np.delete(A, list(S_prime), axis=0)
        A = np.delete(A, list(S_prime), axis=1)

    if k > t * b:
        S_prime = net_shield(A, k - t * b, debug)
        S.update(S_prime)

    return S

# /***********************************************************************/
# / Função para ler arquivo .dot e retornar a matriz de adjacência
# /***********************************************************************/

def read_dot_file(file_path):
    print(f"Lendo arquivo .dot em {file_path}...")
    G = nx.drawing.nx_pydot.read_dot(file_path)
    nodes = list(G.nodes)
    node_map = {node: i for i, node in enumerate(nodes)}
    adj_matrix = nx.adjacency_matrix(G, nodelist=nodes).toarray()
    
    return adj_matrix, node_map

# /***********************************************************************/
# / Main
# /***********************************************************************/

if __name__ == "__main__":

    # Parsing de argumentos da entrada padrão
    parser = argparse.ArgumentParser(description="NetShield+ algorithm implementation")
    parser.add_argument("file_path", type=str, help="Path to the .dot file")
    parser.add_argument("k", type=int, help="Number of nodes to select")
    parser.add_argument("b", type=int, help="Parameter b")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug prints")
    args = parser.parse_args()

    # Chamada do algoritmo
    A, node_map = read_dot_file(args.file_path)
    nodes = netshield_plus(A, args.k, args.b, args.debug)

    # Retorno da resposta
    selected_nodes = [list(node_map.keys())[list(node_map.values()).index(node)] for node in nodes]
    print("Conjunto S:", selected_nodes)
