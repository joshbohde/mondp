#!/usr/bin/python
from main.epsilonMOEA import epsilonMOEA
from mapping.network_mapping import Graph
from main.costChecker import costChecker

def main():
    f = open("cont", 'w')
    c = costChecker.processCostFile('data/rand/rand.cost.xml')
    for i in range(30):
        f.write("Run %s\n" %i)
        g = Graph('data/rand/rand.nod.xml', 'data/rand/rand.edg.xml', 'data/rand/rand.flo.xml')
        g.cost = c
        g.load()
        print g.evaluate()
        e = epsilonMOEA()
        e.setGenome(g)
        e.setNumberofEvals(1000)
        e.initPop(50)
        f.write(e.runEvals())
        f.write("\n\n")
    f.close()


if __name__=="__main__":
    main()
