#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=6
#SBATCH --time=30:00:00
#SBATCH --mem=10GB
#SBATCH --job-name=ARCHS4_SC_Filter
#SBATCH --mail-type=FAIL
#SBATCH --account=pr_284_general
#SBATCH --mail-user=by2372@nyu.edu

module purge
module load python/intel/3.8.6

# Upgrade numpy to meet numba requirements
pip install --user --upgrade 'numpy>=1.22,<1.27'

# Install or verify other packages
pip install --user h5py archs4py

# Use system Python directly
python /scratch/by2372/pipeline/ARCHS4/ARCS4_SC_filter.py

module purge