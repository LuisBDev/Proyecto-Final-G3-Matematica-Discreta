import math
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pprint as pp


# Valores para el grafo: vertices, aristas, posicion
class display_floyd_warshall():
    def main():
        V = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        E = [('A', 'B', 3), ('A', 'F', 5), ('C', 'B', 2), ('B', 'C', 2),
             ('B', 'E', 5), ('C', 'E', 4), ('C', 'D', 8), ('D', 'C', 8),
             ('E', 'F', 3),  ('F', 'A', 5), ('F', 'B', 10), ('H', 'F', 2),
             ('F', 'H', 2),  ('H', 'E', 5), ('G', 'E', 1),  ('G', 'C', 9),
             ('G', 'E', 2), ('E', 'C', 4),  ('E', 'G', 2), ('E', 'B', 1),]
        pos = {'A': [1, 1], 'B': [1, 2], 'C': [1, 3], 'D': [3, 3], 'E': [2, 2], 'F': [2, 1], 'G': [3, 2], 'H': [3, 1]}
        num_nodes = 8

        # Inicializamos el grafo y lo dibujamos
        G = nx.DiGraph()

        G.add_nodes_from(V)

        G.add_weighted_edges_from(E)

        weight = nx.get_edge_attributes(G, 'weight')

        nx.draw_networkx(G, with_labels=True, pos=pos, node_size=1500, node_color='r', edge_color='g', arrowsize=33,
                         font_size=16)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=weight, font_size=16)


        #Generemos la matriz de adyancencia y la imprimimos
        A = nx.to_pandas_adjacency(G)
        print("\nMatriz de adyacencia original con vertices:")
        print(A)

        #Colocamos el grafo a formato de matriz
        adj_matrix = nx.to_numpy_array(G)

        # Colocamos el formato necesario para trabajar la matriz en el algoritmo
        # Si no hay camino directo colocamos un numero alto
        for k in range(num_nodes):
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if adj_matrix[i][j] == 0:
                        adj_matrix[i][j] = math.inf
        np.fill_diagonal(adj_matrix, 0)
        print(f"\nMatriz de adyacencia antes del algoritmo:\n{adj_matrix}")

        # print(adj_matrix[0][1])
        # Algoritmo de Floyd-Warshall para encontrar la matriz de adyacencia optimizada
        for k in range(num_nodes):
            for i in range(num_nodes):
                for j in range(num_nodes):
                    adj_matrix[i][j] = min( adj_matrix[i][j], (adj_matrix[i][k]+adj_matrix[k][j]))

        print(f"\nMatriz de adyacencia optimizada:\n{adj_matrix}")

        print("\n\nCamino minimo entre todos los nodos")
        fw = nx.floyd_warshall(G)
        results = {a: dict(b) for a, b in fw.items()}
        pp.pprint(results)
        plt.show()