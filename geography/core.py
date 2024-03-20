# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['RGG']

# %% ../nbs/00_core.ipynb 3
import numpy as np
import functools
import collections
from fastcore.basics import patch

# %% ../nbs/00_core.ipynb 4
class RGG:
    """random geometric graph"""
    def __init__(self,n:int,r:float, d:int=2):
        self.n = n
        self.r = r
        self.points = np.random.default_rng().random((n,d))
    
    @functools.cached_property
    def distance_matrix(self):
        a = self.points
        diff = a[:,None,:] - a[None,:,:]
        return np.linalg.norm(diff,axis=-1)

    @functools.cached_property
    def adj(self):
        mask = self.distance_matrix < self.r
        return {i: [j for j,v in enumerate(row) if v and j != i] for i,row in enumerate(mask)}
    


# %% ../nbs/00_core.ipynb 8
@patch
def n_comp(self:RGG):
    def dfs(gr,s):
        for v in gr[s]:
            if v not in self.parent:
                self.parent[v]=s
                dfs(gr,v)
                self.topo.append(v)
    self.parent = {}
    self.topo=[]
    count = 0
    for i in range(self.n):
        if i not in self.parent:
            count+=1
            self.parent[i]=None
            dfs(self.adj,i)
            self.topo.append(i)
    return count


# %% ../nbs/00_core.ipynb 10
@patch
def degree_distribution(self: RGG):
    dgr=collections.Counter([len(v) for _,v in self.adj.items()])
    return np.array(list(dgr.items()))

# %% ../nbs/00_core.ipynb 13
@patch
def cyclic(self:RGG):
    for k, lst in self.adj.items():
        for v in lst:
            if k != self.parent[v] and v!=self.parent[k]: 
                return True
    return False

# %% ../nbs/00_core.ipynb 15
@patch
def n_tri(self:RGG):
    A = (self.distance_matrix<=self.r).astype(np.int64)
    np.fill_diagonal(A,0)
    return np.trace(np.linalg.matrix_power(A,3))//6
