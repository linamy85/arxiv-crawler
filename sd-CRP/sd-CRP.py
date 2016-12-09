# Similarity Depenendent Chinese Restaurant Process Mixture Model.
# Implementation of Algorithm 2. from Socher11 paper 
#   (Spectral Chinese Restaurant Processes: Clustering Based on Similarities)
# **Inputs**
#          Y: projected M-dimensional points  Y (y1,...,yN) where N = dim(S),
#          S: Similarity Matrix where s_ij=1 is full similarity and
#                                     s_ij=0 no similarity between observations
#          
# **Outputs**
#          Psi_MAP (MAP Markov Chain State)
#          Psi_MAP.LogProb:
#          Psi_MAP.Z_C:
#          Psi_MAP.clust_params:
#          Psi_MAP.iter:

import sklearn
import numpy as np

from CRP import crpgen

class SDCRP:
    def __init__ (self, S, iter=20, M=20, alpha=1):
        self.S         = S          # similarity matrix
        self.M         = M          # reduced dimension
        self.alpha     = alpha
        self.mu0       = 0
        self.kappa0    = 1
        self.a0        = M   
        self.b0        = M * 0.5
        self.iter      = iter

        self.N = len(S)


    def run (self):
        ### Spectral dimensional reduction
        R = sklearn.manifold.spectral_embedding(self.S, self.M)

        ### Random clustering by CRP
        self.neighbor = []
        table_max = []
        tables = list(crpgen(self.N))
        for cus in range(self.N):
            table = tables[cus]

            if table >= len(table_max):  # not yet met `table`
                table_max.append()
                self.neighbor.append(cus)
            else:  # someone has sit in the table
                self.neighbor.append(table_max[table])
                table_max[table] = cus

        ### Inference for sd-CRP
        for i in range(self.iter):
            for x in np.random.permutation(self.N):
                c_old = self.neighbor[x]

                
            






