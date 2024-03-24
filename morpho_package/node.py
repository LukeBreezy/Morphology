from .point import Point

class Node:

    def __init__(self, level, rep, index, parent=None):
        self.parent = self if parent == None else parent        # Parent Node
        self.index = index                                      # Node Index
        self.rep = rep                                          # Representant
        self.children = []                                      # Children Nodes

        self.level = level                                      # Level / Intensity
        self.cnps = []                                          # Compact Node Pixels

        if not self.isRoot():
            self.parent.addChildren(self)


    def addCnp(self, pixel):
        self.cnps.append(pixel)


    def addChildren(self, node):
        self.children.append(node)


    def isRoot(self):
        return self.rep == self.parent.rep


    def isLeaf(self):
        return not bool(self.childrens)


    def getInfo(self):
        return (
            f"Index: {self.index}\n"
            f"Representant: {self.rep}\n"
            f"Level: {self.level}\n"
            f"Parent: {self.parent.rep}\n"
            f"CNPs: {self.cnps}\n"
            f"Children Nodes: {[child.rep for child in self.children]}"
        )
