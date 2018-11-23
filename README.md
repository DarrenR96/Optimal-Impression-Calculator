# Optimal-Impression-Calculator

A Bi-Stage Optimal Impression Campaign Calculator with G.U.I. for a social media network. Based on the research: "On the Problem of Multi-Staged Impression Allocation in Online Social Networks", by Inzamam Rahaman &amp; Patrick Hosein. Click [here](https://link.springer.com/chapter/10.1007/978-3-319-89932-9_4) to read the research paper.

## Dependencies

This was created and tested using Python3.7 and using the built-in [tkinter library](https://wiki.python.org/moin/TkInter) for the G.U.I.

NetworkX is needed. Find more about NetworkX for python [here](https://networkx.github.io/documentation/stable/index.html). To install with pip:

`pip install networkx`

Matplotlib is also needed to visualize networks. Find out about installation instructions [here](https://matplotlib.org/users/installing.html).

Itertools is also used to perform some combinatorial calculations. Find more about it [here](https://docs.python.org/3/library/itertools.html).

[Numpy](http://www.numpy.org/) & [Itertools](https://docs.python.org/3/library/itertools.html) were also used to do some _fancy_ calculations

---

## Quick How-to Guide

This calculator only finds the objective value for _bi-stage_ impression budgets, i.e. the number of stages can only be two.

1. Clone the directory to your local machine.
   `git clone https://github.com/DarrenR96/Optimal-Impression-Calculator.git`

2. Place your edge-list file in the 'data_sets' folder.

3. Run the main.py python script.
   `python3 main.py`

4. Enter all information and click the _Generate Optimal Assignment_ button.
