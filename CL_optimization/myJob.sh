#!/bin/bash

# Copy/paste this job script into a text file and submit with the command: 
# sbatch filename

#SBATCH --time=120:00:00   # walltime limit (HH:MM:SS)
#SBATCH --nodes=2   # number of nodes
#SBATCH --ntasks-per-node=36   # 36 processor core(s) per node 
#SBATCH --job-name="Oceanauts"
#SBATCH --output="log-%j.txt" # job standard output file (%j replaced by job id)

# LOAD MODULES
. /work/phe/DAFoam_Nova_Gcc/latest/loadDAFoam.sh


#--------------- RUN CODES ---------------

createPatch -overwrite >> logMeshGeneration.txt

renumberMesh -overwrite >> log.meshGeneration    # renumber the mesh for OpenFOAM

cp -r 0.orig 0    # copy initial and boundary condition files

mpirun -np 72 python runScript.py -optimizer=SNOPT    # execute runScript.py
