#!/bin/bash
source ~/.bashrc

module purge
module load intel/19.0.5.281
mpirun /home/ws/gt5111/Celso_QE/qe-6.6/bin/pw.x -inp QEIN.in > QEIN.out
