import networkx as nx
import numpy as np
import itertools as its

alphaVal = 0.15
initProb = 0.25


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
        print("Stage One Expectation:" + str(i.stageOneExpectation))
    print(" ------------------------------------ ")
    print("Total Stage One Possibilites:" + str(count))
    print(" ------------------------------------ ")


class possibleAssignment:
    probDict = {}
    stageOneExpectation = 0
    stageTwoInit = []
    neighborNodes = []

    def __init__(self, ia, firstNodes, firstClick):
        self.impressionVector = ia
        self.firstStageNodes = firstNodes
        self.firstClickArrangements = firstClick
        self.stageTwoPossible = []
        for ln in listOfNodes:
            self.probDict[ln] = initProb
        for fc in self.firstClickArrangements:
            product = 1
            rowTotalExp = 0
            oneSum = 0
            for pc in fc:
                if pc == 0:
                    product = product * (1-initProb)
                if pc == 1:
                    product = product * initProb
                    oneSum += 1
            rowTotalExp = product*oneSum
            self.stageOneExpectation = self.stageOneExpectation + rowTotalExp

    def stageTwoExpectation(self):
        for fc in self.firstClickArrangements:
            counter = 0
            listClick = []
            nb = 0
            for row in fc:
                if row == 0:
                    pass
                if row == 1:
                    listClick.append(self.firstStageNodes[counter])
                counter += 1
            self.stageTwoInit.append([fc, listClick])

        for k in self.stageTwoInit:
            nb = []
            for node in k[1]:
                nb.append(list(G.neighbors(node)))
            self.neighborNodes.append(nb)

        count = 0
        for k in self.stageTwoInit:

            self.stageTwoPossible.append(stageTwoAssignment(
                self.stageOneExpectation, k[1], self.neighborNodes[count], self.probDict))
            count += 1


class stageTwoAssignment:

    def __init__(self, sto, clicknodes, neighbor, dictionary):
        self.neighborNodesUnify = []
        self.stageOneExpectation = sto
        self.clickedNodes = clicknodes
        self.neighborNodes = neighbor
        self.updatedDict = dictionary.copy()
        self.updatedDictList = []
        for n in self.neighborNodes:
            for k in n:
                self.neighborNodesUnify.append(k)
        self.neighborNodesUnify = list(set(self.neighborNodesUnify))
        # print(self.clickedNodes)
        # print(self.updatedDict)
        # print("-----")

        dictionaryProb = self.updatedDict

        for nnu in self.neighborNodesUnify:
            neighborsNNU = list(G.neighbors(nnu))
            totalFriends = len(neighborsNNU)
            counter = 0
            for neigh in neighborsNNU:
                for cn in self.clickedNodes:
                    if neigh == cn:
                        counter += 1
            self.updatedDict[nnu] = 0.25 + alphaVal*(counter/totalFriends)

        print(dictionaryProb)
        print(self.clickedNodes)
        print("-----")
        # 0.25 + alpha(clicked/All)


impressions = 5
stages = 2
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
                    possibleAssignment([i, j], c, clickPossibility))

possibilityObjectVector[10].stageTwoExpectation()
