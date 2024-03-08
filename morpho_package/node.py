from .node_attributes import Attributes
from .point import Point

class Node:

    def __init__(self, level, rep, parent=None):
        self.parent = self if parent == None else parent        # Parent Node
        self.rep = rep                                          # Representant
        self.childrens = {}                                     # Children Nodes

        self.level = level                                      # Level / Intensity
        self.cnps = [rep]                                       # Compact Node Pixels
        self.attributes = Attributes()                          # Node Attributes
        self.top_left = None                                    # Top Left
        self.bottom_right = None                                # Bottom Right


    def addCnp(self, pixel):
        self.cnps.append(pixel)


    def getCnps(self):
        return self.cnps


    def addChildren(self, node):
        self.childrens[node.rep] = node


    def getChildrenNode(self, rep):
        return self.childrens[rep]


    def setTopLeft(self, pixel):
        self.top_left = Point(
            self.top_left.row if self.top_left.row < pixel.row else pixel.row,
            self.top_left.col if self.top_left.col < pixel.col else pixel.col
        )


    def setBottomRight(self, pixel):
        self.bottom_right = Point(
            self.bottom_right.row if self.bottom_right.row > pixel.row else pixel.row,
            self.bottom_right.col if self.bottom_right.col > pixel.col else pixel.col
        )


    def setLimits(self, pixel):
        self.setTopLeft(pixel)
        self.setBottomRight(pixel)


    def isRoot(self):
        return self.rep == self.parent.rep


    def isLeaf(self):
        return not bool(self.childrens)
    

    def preOrderProcess(self):
        self.attributes.preOrderProcess(self)

    
    def inOrderProcess(self):
        self.attributes.inOrderProcess(self)


    def postOrderProcess(self):
        self.attributes.postOrderProcess(self)


    def getInfo(self):
        return (
            f"Representant: {self.rep}\n"
            f"Level: {self.level}\n"
            f"Parent: {self.parent.rep}\n"
            f"CNPs: {self.cnps}\n"
            f"Children Nodes: {list(self.childrens.keys())}\n"
            f"(Top, Left): {self.top_left}\n"
            f"(Bottom, Right): {self.bottom_right}\n"
            f"{self.attributes}"
        )
