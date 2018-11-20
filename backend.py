import networkx as nx
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


def generateNetworkDiagram(dataset):
    try:
        G = nx.read_edgelist('data_sets/'+dataset)
        print(nx.info(G))
        nx.draw(G, with_labels=True)
        plt.show()
    except:
        print("Data-set not found!")
