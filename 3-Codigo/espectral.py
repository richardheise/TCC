#!/bin/python3

import sys
import graphviz
import pydot
import scipy.linalg
import numpy as np
import networkx as nx
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.sparse as sparse
import scipy.sparse.linalg as sla

def print_dot_graph(dot_file):
    # Lendo o arquivo .dot
    G = nx.nx_pydot.read_dot(dot_file)
    G = nx.Graph(G)

    print(G)

    autoVal = nx.laplacian_spectrum(G)
    print(nx.laplacian_matrix(G).toarray())
    autoVal[autoVal < 1e-8] = 0
    print(autoVal)

# Exemplo de uso
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 script.py arquivo.dot")
        sys.exit(1)
        
    dot_file = sys.argv[1]  # Obtendo o nome do arquivo .dot da linha de comando
    print_dot_graph(dot_file)