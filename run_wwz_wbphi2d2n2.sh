#!/bin/bash

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/pdougan/miniforge3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/pdougan/miniforge3/etc/profile.d/conda.sh" ]; then
        . "/home/pdougan/miniforge3/etc/profile.d/conda.sh"
    else
        export PATH="/home/pdougan/miniforge3/bin:$PATH"
    fi
fi
unset __conda_setup

if [ -f "/home/pdougan/miniforge3/etc/profile.d/mamba.sh" ]; then
    . "/home/pdougan/miniforge3/etc/profile.d/mamba.sh"
fi
# <<< conda initialize <<<

conda activate vvv

cd MadLAD
# cd /mnt

export PROC_NAME=wwz_wbphi2d2n2
export MG5_RUN_DIR=gen/$PROC_NAME
export MG5_OUT_DIR=${ClusterId}.${ProcId}.output
export MG5_LOG_DIR=${ClusterId}.${ProcId}.banners

# Initiating
echo -e "launch $MG5_RUN_DIR" > mg5_exec_card

mkdir -p $MG5_OUT_DIR
mkdir -p $MG5_LOG_DIR

# seed=$((ProcId * 30000 + 73 * 10))

python -m madlad.generate --config-name=$PROC_NAME.yaml run.auto-launch=True