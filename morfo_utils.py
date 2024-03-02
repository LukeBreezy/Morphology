# Utilitarios
import numpy as np
import matplotlib.pyplot as plt


# Representa um ponto / pixel na imagem
class Point:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __add__(self, q):
        return Point(self.row + q.row, self.col + q.col)

    def __sub__(self, q):
        return Point(self.row - q.row, self.col - q.col)

    def __eq__(self, q) -> bool:
        return self.row == q.row and self.col == self.col

    def __ne__(self, q) -> bool:
        return not (self == q)

    def __str__(self) -> str:
        return "(" + str(self.row) + ", " + str(self.col) + ")"
    

# Representa uma região ou imagem
class Box:

    # def __init__(self, f):
    # 	height, width = f.shape[0], f.shape[1]

    # 	self.top_left = Point(0, 0)
    # 	self.bottom_right = Point(height-1, width-1)

    # 	assert (self.top_left.row < self.bottom_right.row), "bottom is above top in the plane"
    # 	assert (self.top_left.col < self.bottom_right.col), "left is at right of 'right' in the plane"

    def __init__(self, top_left: Point, bottom_right: Point):
        assert (top_left.row < bottom_right.row), "bottom is above top in the plane"
        assert (top_left.col < bottom_right.col), "left is at right of 'right' in the plane"

        self.top_left = top_left
        self.bottom_right = bottom_right

    def top(self):
        return self.top_left.row

    def left(self):
        return self.top_left.col

    def bottom(self):
        return self.bottom_right.row

    def right(self):
        return self.bottom_right.col

    def width(self):
        return self.bottom_right.col - self.top_left.col + 1

    def height(self):
        return self.bottom_right.row - self.top_left.row + 1

    def contains(self, point: Point):
        return  self.left() <= point.col <= self.right() and self.top() <= point.row <= self.bottom()


# Transforma coordenadas em índices e índices em coordenadas
class PixelIndexer:
    def __init__(self, domain: Box):
        self.domain = domain

    def coord_to_index(self, point: Point):
        q = point - self.domain.top_left
        return self.domain.width() * q.row + q.col

    def index_to_coord(self, index):
        q = Point(index // (self.domain.width()), index % (self.domain.width()))
        return q + self.domain.top_left


# Representa uma vizinhança com adjacência 4
class Adjacency4:
    def __init__(self):
        self.offsets = [
            Point(row=-1, col=0),
            Point(row=0, col=-1),
            Point(row=0, col=1),
            Point(row=1, col=0),
        ]


    def neighbours(self, point: Point) -> list:
        neighbours = []
        for offset in self.offsets:
            q = offset + point
            neighbours.append(q)
        return neighbours


# Representa uma vizinhança com adjacência 8
class Adjacency8:
    def __init__(self):
        self.offsets = [
            Point(row=-1, col=-1),
            Point(row=-1, col=0),
            Point(row=-1, col=1),
            Point(row=0, col=-1),
            Point(row=0, col=1),
            Point(row=1, col=-1),
            Point(row=1, col=0),
            Point(row=1, col=1)
        ]

    def neighbours(self, point: Point) -> list:
        neighbours = []
        for offset in self.offsets:
            q = offset + point
            neighbours.append(q)
        return neighbours


# Algoritmo Union-Find
class UnionFind:
    def __init__ (self, n):
        self.parent = np.arange(n)
        self.size = np.ones((n,), dtype=int)
    
    #find rep with path compression
    def find (self, pixel):
        path = []

        while self.parent[pixel] != pixel:
            pixel = self.parent[pixel]
            path.append(pixel)

        rep = pixel

        for p in path:
            self.parent[p] = rep

        return rep

    #union from (rep of) q to (rep of) p
    def union (self, p, q):
        p_rep = self.find(p)
        q_rep = self.find(q)
        if p_rep != q_rep:
            # make the root of smaller tree point
            # to the root of the larger
            if self.size[p_rep] < self.size[q_rep]:
                self.parent[p_rep] = q_rep
                self.size[q_rep] += self.size[p_rep]
            else:
                self.parent[q_rep] = p_rep
                self.size[p_rep] += self.size[q_rep]


# Rotular componentes conexos
class ConnectedComponents:
    def __init__(self, f, adjacency=Adjacency4()):
        self.image = f
        self.adjacency = adjacency
        self.height = f.shape[0]
        self.width = f.shape[1]

        self.domain = Box(Point(0, 0), Point(self.height - 1, self.width - 1))
        self.union_find = UnionFind(self.height * self.width)
        self.pixel_indexer = PixelIndexer(self.domain)
        self.x_coord, self.y_coord = np.meshgrid(np.arange(self.width), np.arange(self.height))

    def label(self):
        for (row, col) in zip(self.y_coord.ravel(), self.x_coord.ravel()):
            if self.image[row, col] != 0:
                p_point = Point(row, col)
                for q_point in self.adjacency.neighbours(p_point):
                    if self.domain.contains(q_point) and self.image[q_point.row, q_point.col] != 0:
                        p_index = self.pixel_indexer.coord_to_index(p_point)
                        q_index = self.pixel_indexer.coord_to_index(q_point)
                        self.union_find.union(p_index, q_index)

        self.labels = np.zeros((self.height, self.width), dtype='uint8')
        gray_level = 1
        label_dict = {}

        for (row, col) in zip(self.y_coord.ravel(), self.x_coord.ravel()):
            if self.image[row, col] != 0:
                p_index = self.pixel_indexer.coord_to_index(Point(row, col))
                rep = self.union_find.find(p_index)

                if rep not in label_dict: # isso verifica as chaves
                    label_dict[rep] = gray_level
                    gray_level += 1

                self.labels[row, col] = label_dict[rep]


class ComponentTree:
    def __init__(self, f, adjacency):
        self.image = f
        self.adjacency = adjacency

        self.height = self.image.shape[0]
        self.width = self.image.shape[1]

        self.domain = Box(Point(0, 0), Point(self.height - 1, self.width - 1))
        self.pixel_indexer = PixelIndexer(self.domain)
        self.sorted_pixels = self.sortPixels('desc')

        self.x_coord, self.y_coord = np.meshgrid(np.arange(self.width), np.arange(self.height))

        self.parent = np.arange(self.sorted_pixels.shape[0])
        self.zpar = np.full(self.sorted_pixels.shape, None)
        self.canonical_pixels = []


    def sortPixels(self, sort='asc'):
        vector = self.image.flatten()
        sorted_pixels = np.argsort(vector)
        
        if sort == 'desc':
            sorted_pixels = np.flip(sorted_pixels, )

        return sorted_pixels


    def findRoot(self, pixel):
        # if self.zpar[pixel] == pixel:
        #     return pixel
        # else:
        #     return self.findRoot(self.zpar[pixel])
        path = []

        while self.zpar[pixel] != pixel:
            pixel = self.zpar[pixel]
            path.append(pixel)

        rep = pixel

        for p in path:
            self.zpar[p] = rep

        return rep


    def computeTree(self):
        self.zpar = np.full(self.sorted_pixels.shape, None)
        
        for p_index in self.sorted_pixels:
            self.zpar[p_index] = p_index

            p_point = self.pixel_indexer.index_to_coord(p_index)

            for q_point in self.adjacency.neighbours(p_point):
                if self.domain.contains(q_point):
                    q_index = self.pixel_indexer.coord_to_index(q_point)
                    
                    if self.zpar[q_index] != None:
                        root = self.findRoot(q_index)

                        if root != p_index:
                            self.parent[root] = p_index
                            self.zpar[root] = p_index


    def canonize(self):
        for p in np.flip(self.sorted_pixels):
            p_parent = self.parent[p]
            p_grand_parent = self.parent[p_parent]

            p_point = self.pixel_indexer.index_to_coord(p)
            p_parent_point = self.pixel_indexer.index_to_coord(p_parent)
            p_grand_parent_point = self.pixel_indexer.index_to_coord(p_grand_parent)


            if p == p_parent or self.image[p_point.row, p_point.col] != self.image[p_parent_point.row, p_parent_point.col]:
                self.canonical_pixels.append(p)

            if self.image[p_grand_parent_point.row, p_grand_parent_point.col] == self.image[p_parent_point.row, p_parent_point.col]:
                self.parent[p] = p_grand_parent


    def showParents(self):
        ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        if self.sorted_pixels.shape[0] > len(ABC):
            print('Imagem muito grande para a exemplificação')
            return

        imgABC = np.array(list(ABC[0:self.sorted_pixels.shape[0]])).reshape(self.image.shape)

        fig, ax1 = plt.subplots(1, 1, figsize=(5, 5))
        ax1.imshow(self.image, 'gray')

        ax1.get_xaxis().set_visible(False)
        ax1.get_yaxis().set_visible(False)

        for i in range(self.height):
            for j in range(self.width):
                coord = self.pixel_indexer.index_to_coord(self.parent.reshape(self.image.shape)[i, j])
                ax1.text(
                    j, i,
                    f'{imgABC[i, j]} -> {imgABC[coord.row, coord.col]}',
                    color='red',
                    horizontalalignment='center',
                    verticalalignment='center_baseline'
                )

class Node:

    def __init__(self, level, rep, cnps, parent=None):
        self.level = level                                      # Level / Intensity
        self.parent = self if parent == None else parent        # Parent Node
        self.rep = rep                                          # Representant
        self.cnps = []                                          # Compact Node Pixels
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
        return f"Representant: {self.rep} \nParent: {self.parent.rep} \nCNPs: {self.cnps} \nChildren Nodes: {list(self.childrens.keys())}"






def showParents(image, sorted_pixels, parent):
    ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    if sorted_pixels.shape[0] > len(ABC):
        print('Imagem muito grande para a exemplificação')
        return

    imgABC = np.array(list(ABC[0:sorted_pixels.shape[0]])).reshape(image.shape)

    fig, ax1 = plt.subplots(1, 1, figsize=(5, 5))
    ax1.imshow(image, 'gray')

    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)

    height = image.shape[0]
    width = image.shape[1]

    for i in range(height):
        for j in range(width):
            coord = PixelIndexer(
                Box(
                    Point(0, 0),
                    Point(height - 1, width - 1)
                )
            ).index_to_coord(parent.reshape(image.shape)[i, j])

            ax1.text(
                j, i,
                f'{imgABC[i, j]} -> {imgABC[coord.row, coord.col]}',
                color='red',
                horizontalalignment='center',
                verticalalignment='center_baseline'
            )
