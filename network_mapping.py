#!/usr/bin/python
# -*- coding: utf-8 -*-

import elementtree.ElementTree as ET
import random
import time
random.seed(42)

class GraphFactory():
    def __init__(self, nodes_file, edges_file):
        self.n = 0
        self.nodes_file = nodes_file
        self.edges_file = edges_file

    def base_graph(self):
        g = self.graph()
        g.load()
        return g

    def graph(self):
        g = Graph(self.nodes_file, self.edges_file)
        g.id = self.n
        self.n += 1
        g.fact = self
        return g

class Graph():
    def __init__(self, nodes_file=None, edges_file=None ):
        self.nodes = Nodes()
        self.edges = Edges(self.nodes)
        self.nodes_file = nodes_file
        self.edges_file = edges_file

    def load(self):
        self.nodes = Nodes(self.nodes_file)
        self.edges = Edges(self.nodes, self.edges_file)

    def get_files(self):
        return (nodes_file, edges_file)

    def merge(self, other):
        child1 = self.fact.graph()
        child2 = self.fact.graph()
        child1.nodes = self.nodes
        child2.nodes = self.nodes
        for edge in self.edges.get_edges():
            if other.contains_edge(edge):
                child1.add_edge(edge, self.edges.lookup(*edge))
                child2.add_edge(edge, self.edges.lookup(*edge))
            else:
                random.choice((child1, child2)).add_edge(edge, self.edges.lookup(*edge))
        return child1, child2

    def contains_edge(self, edge):
        return self.edges.contains(*edge)

    def add_edge(self, edge, spread):
        self.edges.add(edge[0], edge[1], spread)

    def writexml(self):
        ET.ElementTree(self.nodes.toxml()).write(self.nodes_file + "." + str(self.id))
        ET.ElementTree(self.edges.toxml()).write(self.edges_file + "." + str(self.id))

    def alter_edges(self):
        self.edges.alter(*self.nodes.get_random_pair())

class Nodes():
    def __init__(self, nodes=None):
        self.nodes = {}
        self.mapping = {} #Map new id's to old id's.
        self.n = 0
        if nodes:
            self.load(nodes)

    def load(self, nodes):
        nodes = ET.parse(nodes)
        for node in nodes.getroot().getchildren():
            d = node.attrib
            self.mapping[d["id"]] = str(self.n)
            self.nodes[str(self.n)] = (d["x"], d["y"])
            self.n += 1

    def get_mapped_id(self, id):
        return self.mapping[id]

    def get_random_pair(self):
        return random.sample(self.nodes.keys(), 2)

    def toxml(self):
        xmlnodes = ET.Element("nodes")
        for k, node in self.nodes.items():
            xmlnodes.append(ET.Element("node", id=k, x=str(node[0]), y=str(node[1])))
        return xmlnodes

class Edges():
    def __init__(self, nodes, edges=None):
        self.edges = {}
        self.nodes = nodes
        self.n = 0
        if edges:
            self.load(edges)

    def load(self, edges):
        edges = ET.parse(edges)
        for edge in edges.getroot().getchildren():
            d = edge.attrib
            self.add(self.nodes.get_mapped_id(d["fromnode"]), self.nodes.get_mapped_id(d["tonode"]),  d["spread_type"])

    def add(self, n1, n2, spread):
        key = frozenset((n1, n2))
        self.edges[key] = (str(self.n), spread)
        self.n += 1

    def lookup(self, n1, n2):
        key = frozenset((n1, n2))
        return (self.edges[key])[1]

    def get_edges(self):
        return [tuple(x) for x in self.edges.keys()]

    def alter(self, n1, n2):
        """
        remove the edge is it is found, otherwise make a new one.
        """
        if self.contains(n1, n2):
            del self.edges[frozenset((n1, n2))]
        else:
            self.add(n1, n2, "center")

    def contains(self, n1, n2):
        return frozenset((n1, n2)) in self.edges

    def toxml(self):
        xmledges = ET.Element("edges")
        for k, edge in self.edges.items():
            k = tuple(k)
            xmledges.append(ET.Element("edge", id=edge[0], fromnode=k[0], tonode=k[1], spread_type=edge[1]))
        return xmledges
    
if __name__=="__main__": 
    fact = GraphFactory("hokkaido-japan/hokkaido.nod.xml", "hokkaido-japan/hokkaido.edg.xml")
    g = [fact.base_graph(), fact.base_graph()]
    for d in g:
        d.writexml()
    while len(g) < 100000:
        g.extend(random.choice(g).merge(random.choice(g)))
    print "Starting-----\n"
    start = time.clock()
    for n in g:
        n.merge(random.choice(g))
        n.alter_edges()
    print time.clock() - start
    