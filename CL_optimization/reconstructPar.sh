#!/bin/bash
#SD Reconstruct Par Script

# LOAD MODULES
. /work/phe/DAFoam_Nova_Gcc/latest/loadDAFoam.sh

# RUN CODES
reconstructPar && rm -rf processor*

