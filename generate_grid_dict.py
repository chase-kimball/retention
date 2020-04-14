# coding: utf-8
import numpy as np
import pickle
import sys
import os
runs = sys.argv[1:]
for run in runs:
    raw_grid = np.loadtxt(run).T
    a1, a2, q = [np.unique(param) for param in raw_grid[:3]]
    frac = raw_grid[3].reshape((len(a1), len(a2), len(q)))
    
    grid_dict = dict(a1=a1, a2=a2,q=q,interpolated_retention_fraction=frac)
    print(grid_dict.keys())
    pickle.dump(grid_dict,open(run+'_dict','wb'))
