#!/bin/bash
#SBATCH --account=b1095
#SBATCH --partition=grail-ligo
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time 24:00:00
#SBATCH --mem-per-cpu=3G
#SBATCH --array=0-500%500 # make sure the array number matches the number of lines in your input file!
#SBATCH --error=output/retention_%A_%a.err
#SBATCH --output=output/retention__%A_%a.out
source activate kicks
cd /projects/b1095/chasebk/projects/github/retention
python frac_funcs.py --random-locations-file ../../work/second_gen/plummer_samples/6_A_1.0_M_5E+05 -maxkick -out ../../work/second_gen/retention_grids -N 100000 --label maxkick_huge -Na 100 -Nq 100 --Nbatch 499 --batch ${SLURM_ARRAY_TASK_ID}
