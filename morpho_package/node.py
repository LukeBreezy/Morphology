from .node_attributes import Attributes


class Node:

    def __init__(self, level, rep, parent=None):
        self.parent = self if parent == None else parent        # Parent Node
        self.rep = rep                                          # Representant
        self.childrens = {}                                     # Children Nodes

        self.level = level                                      # Level / Intensity
        self.cnps = [rep]                                       # Compact Node Pixels
        self.attributes = Attributes()                          # Node Attributes


    def addCnp(self, pixel):
        self.cnps.append(pixel)


    def getCnps(self):
        return self.cnps


    def addChildren(self, node):
        self.childrens[node.rep] = node


    def getChildrenNode(self, rep):
        return self.childrens[rep]


    def isRoot(self):
        return self.rep == self.parent.rep


    def isLeaf(self):
        return not bool(self.childrens)
    

    def computeAttributes(self):
        self.attributes.computeAttributes(self)


    def getInfo(self):
        return (
            f"Representant: {self.rep}\n"
            f"Level: {self.level}\n"
            f"Parent: {self.parent.rep}\n"
            f"CNPs: {self.cnps}\n"
            f"Children Nodes: {list(self.childrens.keys())}\n"
            f"{self.attributes}"
        )
