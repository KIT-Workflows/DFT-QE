#!/bin/bash
source ~/.bashrc

module purge
module load intel/19.0.5.281
module load mpich/3.3.1

mpirun /shared/software/chem/qe/7.1/bin/pw.x -inp input.pwi > QEIN.out