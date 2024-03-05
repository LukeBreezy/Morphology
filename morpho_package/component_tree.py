import numpy as np
import matplotlib.pyplot as plt

from .point import Point
from .adjacency import *
from .box import Box
from .pixel_indexer import PixelIndexer


class ComponentTree:
    def __init__(self, f, adjacency):
        self.image = f
        self.adjacency = adjacency

        self.height = self.image.shape[0]
        self.width = self.image.shape[1]

        self.domain = Box(Point(0, 0), Point(self.height - 1, self.width - 1))
        self.pixel_indexer = PixelIndexer(self.domain)
        self.sorted_pixels = self.sortPixels()

        # self.x_coord, self.y_coord = np.meshgrid(np.arange(self.width), np.arange(self.height))

        # self.parent = np.arange(self.sorted_pixels.shape[0])
        # self.zpar = np.full(self.sorted_pixels.shape, None)


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
        self.parent = np.full(self.sorted_pixels.shape, None)
        self.zpar = np.full(self.sorted_pixels.shape, None)

        # print(f'parent: {self.parent}')
        # print(f'zpar: {self.zpar}')

        for p_index in self.sorted_pixels:
            self.parent[p_index] = self.zpar[p_index] = p_index

            p_point = self.pixel_indexer.indexToCoord(p_index)

            for q_point in self.adjacency.neighbours(p_point):
                if self.domain.contains(q_point):
                    q_index = self.pixel_indexer.coordToIndex(q_point)
                    
                    if self.zpar[q_index] != None:
                        root = self.findRoot(q_index)

                        if root != p_index:
                            self.parent[root] = p_index
                            self.zpar[root] = p_index


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
                coord = self.pixel_indexer.indexToCoord(self.parent.reshape(self.image.shape)[i, j])
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
