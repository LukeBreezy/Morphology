class Attributes:

    def __init__(self):
        self.area = 0
        self.volume = 0


    def computeAttributes(self, node):
        self.computeArea(node)
        self.computeVolume(node)


    def computeArea(self, node):
        self.area += len(node.cnps)

        if node.isRoot():
            return

        node.parent.attributes.area += self.area


    def computeVolume(self, node):
        self.volume += len(node.cnps) * node.level

        if node.isRoot():
            return

        node.parent.attributes.volume += self.volume


    def __str__(self):
        return (
            f"Area: {self.area}\n"
            f"Volume: {self.volume}"
        )
