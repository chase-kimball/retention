#!/bin/bash
#SBATCH --account=b1095
#SBATCH --partition=grail-ligo
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=5:00:00
#SBATCH --mem-per-cpu=3G


cd ../../github/retention
python frac_funcs.py --random-locations-file plummer_samples/5_A_1.0_M_5E+05 -maxkick -out ../../work/retention_grids -N 10000 --label maxkick -Na 100 -Nq 100
