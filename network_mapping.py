#!/usr/bin/python

import xml.dom.minidom as xml


class Graph():
    def __init__(self, nodes_file, edges):
        dom_node = Nodes(nodes_file)
        print dom_node.toxml()
        
        
class Node():
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    
    def __str__(self):
        return 'x="' + str(self.x) + ' y="' + str(self.y)
        
class Nodes():
    def __init__(self, nodes):
        self.nodes = {}
        dom_nodes = xml.parse(nodes)
        for node in dom_nodes.getElementsByTagName('node'):
            self.nodes[node.getAttribute("id")] = Node(node.getAttribute("x"), node.getAttribute("y"))
            print node.getAttribute("id"), ": (", self.nodes[node.getAttribute("id")], ")"
            
    def toxml(self):
        xmlnodes = xml.Node()
        for k, node in self.nodes.items():
            e = xml.Element("1")
            e.setAttribute("id", k)
            e.setAttribute("x", node.x)
            e.setAttribute("y", node.y) 
            xmlnodes.appendChild(e)
        return xmlnodes
            
        
class Edge():
    def __init__(self, name, from_node, to_node, spread):
        pass
    
if __name__=="__main__": 
    g = Graph("hokkaido-japan/hokkaido.nod.xml", "foo")