class Node:

    def __init__(self, level, rep, parent=None):
        self.level = level                                      # Level / Intensity
        self.parent = self if parent == None else parent        # Parent Node
        self.rep = rep                                          # Representant
        self.cnps = [rep]                                       # Compact Node Pixels
        self.childrens = {}                                     # Children Nodes


    def addCnp(self, pixel):
        self.cnps.append(pixel)


    def getCnps(self):
        return self.cnps


    def addChildren(self, node):
        self.childrens[node.rep] = node


    def getChildrenNode(self, rep):
        return self.childrens[rep]


    def getChildrens(self):
        return self.childrens
    

    def getInfo(self):
        return f"Representant: {self.rep} \nLevel: {self.level} \nParent: {self.parent.rep} \nCNPs: {self.cnps} \nChildren Nodes: {list(self.childrens.keys())}"
