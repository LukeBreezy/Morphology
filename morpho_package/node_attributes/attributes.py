class Attributes:

    def __init__(self):
        self.area = None
        self.volume = None
        self.height = None
        self.width = None


    # Pré-ordem
    def preOrderProcess(self, node):
        self.preOrderArea(node)
        self.preOrderVolume(node)


    def preOrderArea(self, node):
        self.area = len(node.cnps)


    def preOrderVolume(self, node):
        self.volume = len(node.cnps) * node.level


    # Ordem
    def inOrderProcess(self, node):
        self.inOrderArea(node)
        self.inOrderVolume(node)
        self.inOrderTopLef(node)
        self.inOrderBottomRigh(node)


    def inOrderArea(self, node):
        node.parent.attributes.area += self.area


    def inOrderVolume(self, node):
        node.parent.attributes.volume += self.volume


    def inOrderTopLef(self, node):
        node.parent.setTopLeft(node.top_left)

    
    def inOrderBottomRigh(self, node):
        node.parent.setBottomRight(node.bottom_right)


    # Pós-Ordem
    def postOrderProcess(self, node):
        self.postOrderHeight(node)
        self.postOrderWidth(node)

    
    def postOrderHeight(self, node):
        self.height = node.bottom_right.row - node.top_left.row + 1


    def postOrderWidth(self, node):
        self.width = node.bottom_right.col - node.top_left.col + 1


    def __str__(self):
        return (
            f"Area: {self.area}\n"
            f"Volume: {self.volume}\n"
            f"Height: {self.height}\n"
            f"Width: {self.width}"
        )
