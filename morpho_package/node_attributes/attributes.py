from ..node import Node

class Attribute:

    def __init__(self, attr_name, node: Node):
        self.attr_name = attr_name
        self.node = node
        self.computeAttribute()


    def computeAttribute(self):
        if not self.hasAttribute(self.node):
            self.node.attributes[self.attr_name] = 0


    def hasAttribute(self, node):
        return self.attr_name in node.attributes.keys()


class Area(Attribute):

    def __init__(self, node: Node):
        super().__init__('area', node)


    def computeAttribute(self):
        super().computeAttribute()
        self.node.attributes[self.attr_name] += len(self.node.cnps)

        if self.node.isRoot():
            return

        if not self.hasAttribute(self.node.parent):
            self.node.parent.attributes[self.attr_name] = 0

        self.node.parent.attributes[self.attr_name] += self.node.attributes[self.attr_name]


class Volume(Attribute):

    def __init__(self, node: Node):
        super().__init__('volume', node)


    def computeAttribute(self):
        super().computeAttribute()
        self.node.attributes[self.attr_name] += len(self.node.cnps) * self.node.level

        if self.node.isRoot():
            return

        if not self.hasAttribute(self.node.parent):
            self.node.parent.attributes[self.attr_name] = 0

        self.node.parent.attributes[self.attr_name] += self.node.attributes[self.attr_name]

