from tkinter import *
import networkx as nx
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


G = nx.read_edgelist('data_sets/example_network.txt')
print(nx.info(G))

nx.draw(G, with_labels=True)
plt.show()

root = Tk()

root.mainloop()
