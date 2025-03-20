import os
import glob
import gzip
import re

import subprocess
from pathlib import Path
from madlad.parameters import edit_madspin

from omegaconf import DictConfig

def gunzip_file(filepath):
    with gzip.open(filepath, 'rb') as f_in:
        with open(filepath[:-3], 'wb') as f_out:
            f_out.write(f_in.read())

def gzip_file(filepath):
    with open(filepath, 'rb') as f_in:
        with gzip.open(filepath + '.gz', 'wb') as f_out:
            f_out.write(f_in.read())

def sed_file(filepath, patterns):
    with open(filepath, 'r') as file:
        filedata = file.read()
    
    for pattern, repl in patterns:
        filedata = re.sub(pattern, repl, filedata)
    
    with open(filepath, 'w') as file:
        file.write(filedata)

def runMadspinSA(cfg : DictConfig, dir: str, run_with: str, image_name: str, logger) -> None:
    r"""Run Madspin Decay Standalone.
    """
    if 'run_standalone' in list(cfg['gen']['block_madspin'].keys()):
        if cfg['gen']['block_madspin']['run_standalone'] == True:

            logger.info("Hack: Removing NP from cards for Madspin.")

            evt_dir = 'run_01'
            lhetar_path = glob.glob(f'{dir}/Events/{evt_dir}/*.lhe.gz')[0]
            gunzip_file(lhetar_path)
            lhe_path = glob.glob(f'{dir}/Events/{evt_dir}/*.lhe')[0]
            
            # Modify the LHE file
            lhe_patterns = [
                (r'NP(BIS)?=+[0-9]', ''),
                (r'NP(BIS)?\^2=+[0-9]', ''),
                (r'add process.*', '')
            ]
            sed_file(lhe_path, lhe_patterns)

            # Zip the LHE file
            gzip_file(lhe_path)
            
            proccard_path = glob.glob(f'{dir}/Cards/proc_card_mg5.dat')[0]
            # Modify the proc card file
            proccard_patterns = [
                (r'NP(BIS)?=+[0-9]', ''),
                (r'NP(BIS)?\^2=+[0-9]', ''),
                (r'add process.*', '')
            ]
            sed_file(proccard_path, proccard_patterns)

            if 'block_madspin' in list(cfg['gen'].keys()):
                logger.info('Editing MG5 MadSpin card.')
                edit_madspin(cfg)

            logger.info("Running decay with Madspin.")

            save_dir = cfg['gen']['block_model']['save_dir']
            madspin_card_loc = os.path.join(save_dir, "Cards", "madspin_card.dat")

            logger.info('Running madspin standalone.')
            ecard = open(f"madspin_exec_card-{os.path.basename(dir)}","w")
                
            # ecard.write(f"#!/bin/bash\n/app/MG5_aMC/MadSpin/madspin {madspin_card_loc}")
            ecard.write(f"launch {dir} -i\ndecay_events {evt_dir}")

            ecard.close()

            if run_with == "docker":
                logger.info('Running post commands using Docker.')
                subprocess.run(
                [
                    "docker", "run", "--rm", "-it", "-w", "/home/atreus/data",
                    "-v", f"{Path().absolute()}:/home/atreus/data",
                    image_name, cfg['run']['mg5'],
                    f"bash madspin_exec_card-{os.path.basename(dir)}"
                ]
            )

            if run_with == "singularity":
                logger.info('Running post commands using Singularity.')
                subprocess.run(
                [
                    "singularity", "exec", "--bind", f"{Path().absolute()}",
                    image_name, cfg['run']['mg5'],
                    f"madspin_exec_card-{os.path.basename(dir)}"
                ]
            )

            # decaytar_path = glob.glob(f'{dir}/Events/{evt_dir}/*decayed.lhe.gz')[0]
            # os.system(f'mv {decaytar_path} {dir}/Events/run_01_decayed_1/unweighted_events.lhe.gz')
            # decaybanner_path = glob.glob(f'{dir}/Events/{evt_dir}/{evt_dir}_tag_1_banner.txt')[0]
            # os.system(f'mv {decaybanner_path} {dir}/Events/run_01_decayed_1/run_01_decayed_1_tag_1_banner.txt')
