import networkx as nx
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import itertools as its
import numpy as np
import operator

# Classes
impressions = None
stages = None
clickVector = None
alphaVal = None
initProb = None
array = None
finalArray = None
temp2 = None
G = None
numberOfNodes = None
listOfNodes = None


class possibleAssignment:
    probDict = {}
    stageOneExpectation = 0

    def __init__(self, ia, firstNodes, firstClick):
        self.val = 0
        self.optimum = 0
        self.impressionVector = ia
        self.firstStageNodes = firstNodes
        self.firstClickArrangements = firstClick
        self.stageTwoPossible = []
        self.stageTwoInit = []
        self.neighborNodes = []
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
        copyInit = []
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
        # print(self.stageTwoInit)
        for k in self.stageTwoInit:
            nb = []
            for node in k[1]:
                nb.append(list(G.neighbors(node)))
            self.neighborNodes.append(nb)

        count = 0
        for k in self.stageTwoInit:

            self.stageTwoPossible.append(stageTwoAssignment(
                self.stageOneExpectation, k[1], self.neighborNodes[count], self.probDict, self.impressionVector, k[0]))
            count += 1

        self.rowTot = 0
        temp1 = 0
        templist = []
        for j in self.stageTwoPossible:
            templist.append(j.finalOut)
        temp1 = sum(templist)
        finalArray.append(
            ((temp1+self.stageOneExpectation),
             (self.impressionVector), (self.firstStageNodes)))


class stageTwoAssignment:

    def __init__(self, sto, clicknodes, neighbor, dictionary, iv, fca):
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
        self.total = []
        # print(self.clickedNodes)
        # print(self.updatedDict)
        # print("-----")
        self.firstClickPoss = fca

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
        # print(self.flattened)
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
        rowTotal = 0
        # print(self.clickedNodes)
        # # print(self.secondStageExp)
        # print(self.impressionVector)
        # print(self.firstClickPoss)
        # print(self.clickPossibility)
        product = 1
        for k in self.firstClickPoss:
            if k == 0:
                product *= (1-initProb)
            if k == 1:
                product *= (initProb)
        self.probabilityOccurOne = product
        # print('Probab:' + str(self.probabilityOccurOne))
        # print('SecondStage:' + str(self.secondStageExp))
        # print('----')
        self.finalOut = (self.probabilityOccurOne * self.secondStageExp)

        # print(self.probabilityOccurOne)
        # print(self.secondStageExp)

        # print('--------')

# Funcs


def generateNetworkDiagram(dataset):
    try:
        G = nx.read_edgelist('data_sets/'+dataset)
        print(nx.info(G))
        nx.draw(G, with_labels=True)
        plt.show()
    except:
        print("Data-set not found!")


# Main

def runMain(dataset, imps, alpha, prob):
    global impressions
    impressions = imps
    global stages
    stages = 2
    global clickVector
    clickVector = np.array([0, 1])
    global alphaVal
    alphaVal = alpha
    global initProb
    initProb = prob
    global array
    array = 0
    global finalArray
    finalArray = []
    global temp2
    temp2 = 0
    global G
    G = nx.read_edgelist('data_sets/'+dataset)
    global numberOfNodes
    numberOfNodes = G.number_of_nodes()
    global listOfNodes
    listOfNodes = G.nodes()

    possibilityObjectVector = []
    for i in range(1, impressions):
        for j in range(1, impressions):
            if (i+j == impressions):
                combs = its.combinations(listOfNodes, i)
                clickPossibility = list(its.product(clickVector, repeat=i))
                for c in combs:
                    possibilityObjectVector.append(
                        possibleAssignment([i, j], c, clickPossibility))

    for j in possibilityObjectVector:
        j.stageTwoExpectation()

    finalArray.sort(key=lambda x: x[0])
    return (finalArray.pop())


runMain('example_network.txt', 5, 0.15, 0.25)
