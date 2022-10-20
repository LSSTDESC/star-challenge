#!/bin/bash

#SBATCH -t 36:00:00
#SBATCH --partition=broadwl
#SBATCH --account=pi-chihway
##SBATCH --ntasks=100
#SBATCH --nodes=6
#SBATCH --cpus-per-task=1
#SBATCH --job-name=3x2_real
#SBATCH --exclusive

#module load python
#conda activate firecrown
#module load openmpi/3.1.4

source setup.sh

mpirun -n 200 cosmosis --mpi cosmosis/gaussian_sims_3x2pt_real_w0-wa.ini  -p runtime.sampler='emcee'

