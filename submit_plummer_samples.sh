#!/bin/bash
#SBATCH --account=b1095
#SBATCH --partition=grail-ligo
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=5:00:00
#SBATCH --mem-per-cpu=3G



python get_R_Vescs.py --mass 5e5 --radius 1.0 --Nsamps 100000
