from .attributes import *

class ComputeAttributes:

    def __init__(self, nodes):
        self.nodes = nodes
        self.computeIncrementalAttributes()


    def computeIncrementalAttributes(self):
        for node_key in self.nodes.__reversed__():
            Area(self.nodes[node_key])
            Volume(self.nodes[node_key])

