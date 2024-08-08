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

export PROC_NAME=wz_cHWB_int
export MG5_RUN_DIR=gen/$PROC_NAME
export MG5_OUT_DIR=${ClusterId}.${ProcId}.output
export MG5_LOG_DIR=${ClusterId}.${ProcId}.banners

# Initiating
echo -e "launch $MG5_RUN_DIR" > mg5_exec_card

mkdir -p $MG5_OUT_DIR
mkdir -p $MG5_LOG_DIR

# seed=$((ProcId * 30000 + 73 * 10))

python -m madlad.generate --config-name=$PROC_NAME.yaml run.auto-launch=True

#Madspin doesn't run with squared couplings, here is hack to trick Madspin by removing the NP coupling order in the process
lhetar_path=$MG5_RUN_DIR/Events/run_01/unweighted_events.lhe.gz
lhe_path=$MG5_RUN_DIR/Events/run_01/unweighted_events.lhe
proccard_path=$MG5_RUN_DIR/Cards/proc_card_mg5.dat

gunzip $lhetar_path
sed -i -r 's/NP=+[0-9]//g' $lhe_path
sed -i -r 's/NP\^2=+[0-9]//g' $lhe_path
sed -i -r 's/add process.*//g' $lhe_path
gzip $lhe_path
sed -i -r 's/NP=+[0-9]//g' $proccard_path
sed -i -r 's/NP\^2=+[0-9]//g' $proccard_path
sed -i -r 's/add process.*//g' $proccard_path

# echo -e "launch madspin_sa.sh $PROC_NAME" > madspin_exec_card

sed -i "s#gen/gen_name/Events/run_01/unweighted_events.lhe.gz#gen/${PROC_NAME}/Events/run_01/unweighted_events.lhe.gz#g" madspin_sa.sh

singularity exec --no-home --bind $PWD:/mnt ../madlad-custom-patrick.sif bash /mnt/run_madspin.sh

# cp -r gen/* /home/pdougan/EventGeneration/condor/