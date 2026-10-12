#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=15:00:00
#SBATCH --mem=30GB
#SBATCH --job-name=ARCHS4_Filter_1_2_3
#SBATCH --mail-type=FAIL
#SBATCH --account=torch_pr_44_general
#SBATCH --mail-user=by2372@nyu.edu

module purge

singularity exec --nv \
	    --overlay /scratch/by2372/ML_envir/ML_envir.ext3:ro \
	    /share/apps/images/cuda12.1.1-cudnn8.9.0-devel-ubuntu22.04.2.sif \
	    /bin/bash -c "source /ext3/env.sh; python ARCHS4_Filter_1_2_3.py"

module purge