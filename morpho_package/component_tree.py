import numpy as np
import matplotlib.pyplot as plt

from .point import Point
from .adjacency import *
from .box import Box
from .pixel_indexer import PixelIndexer
from .image import Image
from .union_find import UnionFind


class ComponentTree:

    def __init__(self, f, adjacency):
        self.image = Image(f)
        self.union_find = UnionFind(self.image.flatten.shape)
        self.adjacency = adjacency
        self.sorted_pixels = self.sortPixels()


    def sortPixels(self, sort='asc'):
        vector = self.image.flatten
        sorted_pixels = np.argsort(vector)
        
        if sort == 'desc':
            sorted_pixels = np.flip(sorted_pixels)

        return sorted_pixels


    def computeTree(self):
        for p_index in self.sorted_pixels:
            self.union_find.parent[p_index] = self.union_find.zpar[p_index] = p_index

            p_point = self.image.indexToCoord(p_index)

            for q_point in self.adjacency.neighbours(p_point):
                if self.image.contains(q_point):
                    q_index = self.image.coordToIndex(q_point)
                    
                    if self.union_find.zpar[q_index] != None:
                        self.union_find.union(p_index, q_index)


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

        for i in range(self.image.height):
            for j in range(self.image.width):
                coord = self.image.indexToCoord(self.union_find.parent.reshape(self.image.shape)[i, j])
                ax1.text(
                    j, i,
                    f'{imgABC[i, j]} -> {imgABC[coord.row, coord.col]}',
                    color='red',
                    horizontalalignment='center',
                    verticalalignment='center_baseline'
                )


class UpperLevelSets(ComponentTree):
        
    def sortPixels(self):
        return super().sortPixels('desc')


class LowerLevelSets(ComponentTree):
    
    def sortPixels(self):
        return super().sortPixels('asc')



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
            ).indexToCoord(parent.reshape(image.shape)[i, j])

            ax1.text(
                j, i,
                f'{imgABC[i, j]} -> {imgABC[coord.row, coord.col]}',
                color='red',
                horizontalalignment='center',
                verticalalignment='center_baseline'
            )
