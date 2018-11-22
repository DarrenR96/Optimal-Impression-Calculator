import networkx as nx
import numpy as np
import itertools as its
import operator

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
                self.stageOneExpectation, k[1], self.neighborNodes[count], self.probDict, self.impressionVector))
            count += 1


class stageTwoAssignment:

    def __init__(self, sto, clicknodes, neighbor, dictionary, iv):
        self.secondStageExp = 0
        self.impressionVector = iv
        self.neighborNodesUnify = []
        self.stageOneExpectation = sto
        self.clickedNodes = clicknodes
        self.neighborNodes = neighbor
        self.updatedDict = dictionary.copy()
        self.selectedStageTwoNodes = []
        for n in self.neighborNodes:
            for k in n:
                self.neighborNodesUnify.append(k)
        self.neighborNodesUnify = list(set(self.neighborNodesUnify))
        # print(self.clickedNodes)
        # print(self.updatedDict)
        # print("-----")

        for nnu in self.neighborNodesUnify:
            neighborsNNU = list(G.neighbors(nnu))
            totalFriends = len(neighborsNNU)
            counter = 0
            for neigh in neighborsNNU:
                for cn in self.clickedNodes:
                    if neigh == cn:
                        counter += 1
            self.updatedDict[nnu] = 0.25 + alphaVal*(counter/totalFriends)
        for cn in self.clickedNodes:
            del self.updatedDict[cn]

        [n1, n2] = self.impressionVector
        self.sortedClicks = sorted(self.updatedDict.items(),
                                   key=operator.itemgetter(1), reverse=True)
        self.clickPossibility = list(its.product(clickVector, repeat=n2))
        list2 = []
        for i in range(0, n2):
            list2.append(self.sortedClicks[i])
        self.selectedStageTwoNodes.append(list2)
        rowTotal = 0
        self.flattened = []
        for sublist in self.selectedStageTwoNodes:
            for val in sublist:
                self.flattened.append(val)
        print(self.flattened)
        for cp in self.clickPossibility:
            rowCounter = 0
            oneCounter = 0
            product = 1
            for i in cp:
                if i == 1:
                    product = product * self.flattened[rowCounter][1]
                    oneCounter += 1
                    pass
                if i == 0:
                    product = product * (1-self.flattened[rowCounter][1])

                    pass
                rowCounter += 1
            rowTotal = oneCounter*product
            self.secondStageExp += rowTotal
        print(self.secondStageExp)
        # Row Sum


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

possibilityObjectVector[100].stageTwoExpectation()
