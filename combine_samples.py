import numpy as np
import glob 
import sys
import os
runs = sys.argv[1:]
for run in runs:
    print(run)
    grid = []
    batchfiles = glob.glob(os.path.join(run,'*'))
    for ii in range(len(batchfiles)):
        grid.extend(np.loadtxt(os.path.join(run,'retention_fractions_'+str(ii))))

    np.savetxt(run+'_all', grid)


