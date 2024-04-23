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

def simple_hash(value, alpha):
    return value % alpha

def SummaryGraph(A, alpha):
    n = len(A)
    C = np.zeros((alpha, alpha))
    
    for i in range(n):
        for j in range(i, n):
            if A[i][j] == 1:
                hash_i = simple_hash(i, alpha)
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
        
        for v in range(n):
            dG_v = np.sum(A[v])  # Calcula o grau do vértice v em A(G)
            C6 = np.sum(np.power(Ci[v], 6))  # Soma dos elementos da sexta potência de Ci[v]
            C4 = np.sum(np.power(Ci[v], 4))  # Soma dos elementos da quarta potência de Ci[v]
            C3 = np.sum(np.power(Ci[v], 3))  # Soma dos elementos da terceira potência de Ci[v]
            
            D6 = np.sum(np.power(np.sum(Ci, axis=1), 6))  # Soma dos graus elevados à sexta potência
            D4 = np.sum(np.power(np.sum(Ci, axis=1), 4))  # Soma dos graus elevados à quarta potência
            D3 = np.sum(np.power(np.sum(Ci, axis=1), 3))  # Soma dos graus elevados à terceira potência
            
            cw_prime_i[v] = (6 * C6 * D6 - 6 * dG_v * C4 * D4 - 3 * np.power(C3 * dG_v / D3, 2) + 2 * np.power(dG_v, 3))
        
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