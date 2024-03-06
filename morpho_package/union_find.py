import numpy as np

class UnionFind:

    def __init__(self, vector_size):
        self.parent = np.full(vector_size, None)
        self.zpar = np.full(vector_size, None)


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


    def union(self, p_index, q_index):
        root = self.findRoot(q_index)

        if root != p_index:
            self.parent[root] = p_index
            self.zpar[root] = p_index
