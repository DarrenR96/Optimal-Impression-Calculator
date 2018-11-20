import networkx as nx
import numpy as np
import itertools as its


def printStageOnePoss():
    count = 0
    for i in possibilityObjectVector:
        count += 1
        print(" ------------------------------------ ")
        print("Impression Vector:" + str(i.impressionVector))
        print("First Stage Node Selection:" + str(i.firstStageNodes))
        print("Click possibilites:")
        for cp in (i.firstClickArrangements):
            print(cp)
    print(" ------------------------------------ ")
    print("Total Stage One Possibilites:" + str(count))
    print(" ------------------------------------ ")


class possibleAssignment:
    def __init__(self, ia, firstNodes, firstClick):
        self.impressionVector = ia
        self.firstStageNodes = firstNodes
        self.firstClickArrangements = firstClick


impressions = 5
stages = 2
initProb = 0.25
alpha = 0.15
clickVector = np.array([0, 1])

G = nx.read_edgelist('data_sets/example_network.txt')
numberOfNodes = G.number_of_nodes()
listOfNodes = G.nodes()


# Generate Impression Alogrithm based on impressions

possibilityObjectVector = []
for i in range(1, impressions):
    for j in range(1, impressions):
        if (i+j == impressions):
            combs = its.combinations(listOfNodes, i)
            clickPossibility = list(its.product(clickVector, repeat=i))
            for c in combs:
                possibilityObjectVector.append(
                    possibleAssignment([i, j], [c], clickPossibility))

printStageOnePoss()
