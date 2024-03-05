from .attributes import *


class ComputeAttributes:

    def __init__(self, nodes):
        self.computeIncrementalAttributes(nodes)


    def computeIncrementalAttributes(self, nodes):
        for node_key in nodes.__reversed__():
            node = nodes[node_key]
            node.computeAttributes()

