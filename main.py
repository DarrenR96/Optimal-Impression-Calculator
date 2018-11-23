import backend
from tkinter import *

result = None


def popupmsg(msg):
    popup = Tk()
    popup.wm_title("Optimal Assignment!")
    maxValue = Label(popup, text='Objective Value = ' + str(msg[0]))
    maxValue.pack(side="top", fill="x", pady=10)
    assignmentVector = Label(popup, text='Impression Vector = ' + str(msg[1]))
    assignmentVector.pack(side="top", fill="x", pady=10)
    chosenFriends = Label(popup, text='Chosen Nodes = ' + str(msg[2]))
    chosenFriends.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def guiNetworkDiagramHandler():
    dataSet = dataEntry.get()
    backend.generateNetworkDiagram(dataSet)


def genOptimal():
    dataSet = dataEntry.get()
    impressions = int(impressionEntry.get())
    alpha = float(alphaEntry.get())
    prob = float(probEntry.get())
    global result
    result = backend.runMain(dataSet, impressions, alpha, prob)
    popupmsg(result)


root = Tk()

root.geometry('600x600')
root.title('Optimal Impression Calculator')
root.configure(background='#f0f5f9')

titleFrame = Frame(root)
titleFrame.pack(side=TOP, pady=20)
textLabel = Label(titleFrame, text="Optimal Impression Calculator",
                  font="Kollektif 25 bold", background='#f0f5f9')
textLabel.pack()

impressionFrame = Frame(root, background='#f0f5f9')
impressionFrame.pack()
impressionText = Label(
    impressionFrame, text='Number of Impressions in Budget:', font="Kollektif", background='#f0f5f9')
impressionText.pack(padx=40, pady=20, side=LEFT)
impressionEntry = Entry(impressionFrame)
impressionEntry.pack(pady=20, side=LEFT)

stagesFrame = Frame(root, background='#f0f5f9')
stagesFrame.pack()
stagesLabel = Label(
    stagesFrame, text='Number of Stages:', font="Kollektif", background='#f0f5f9')
stagesLabel.pack(padx=40, pady=20, side=LEFT)
stagesEntry = Entry(stagesFrame)
stagesEntry.insert(0, 2)
stagesEntry.configure(state="disabled")
stagesEntry.pack(pady=20, side=LEFT)


probFrame = Frame(root, background='#f0f5f9')
probFrame.pack()
probLabel = Label(
    probFrame, text='Initial Prob. of clicking:', font="Kollektif", background='#f0f5f9')
probLabel.pack(padx=40, pady=20, side=LEFT)
probEntry = Entry(probFrame)
probEntry.pack(pady=20, side=LEFT)

dataFrame = Frame(root, background='#f0f5f9')
dataFrame.pack()
dataLabel = Label(
    dataFrame, text='Data-set file name:', font="Kollektif", background='#f0f5f9')
dataLabel.pack(padx=40, pady=20, side=LEFT)
dataEntry = Entry(dataFrame)
dataEntry.pack(pady=20, side=LEFT)

alphaFrame = Frame(root, background='#f0f5f9')
alphaFrame.pack()
alphaLabel = Label(
    alphaFrame, text='Alpha value:', font="Kollektif", background='#f0f5f9')
alphaLabel.pack(padx=40, pady=20, side=LEFT)
alphaEntry = Entry(alphaFrame)
alphaEntry.pack(pady=20, side=LEFT)

calculateOptimalButton = Button(
    root, text="Generate Optimal Assignment", command=genOptimal
)
calculateOptimalButton.pack(pady=10)
generateNetworkButton = Button(
    root, text='Generate Network Diagram', command=guiNetworkDiagramHandler)
generateNetworkButton.pack(pady=20)

root.mainloop()
