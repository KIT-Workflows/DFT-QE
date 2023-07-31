#!/bin/bash

# read the values of source and conda keys from the YAML file
# source_path=$(grep -Po '(?<=source": ")[^"]*' conda_env.yml)
# conda_activate=$(grep -Po '(?<=conda": ")[^"]*' conda_env.yml)

# execute the command using the extracted values
source /home/ws/gt5111/miniconda3/etc/profile.d/conda.sh
conda activate

python qe-inputs.py
bash run_QE.sh 		
python get_properties.py