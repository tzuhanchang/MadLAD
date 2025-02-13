import os
import glob

import subprocess
from pathlib import Path

from omegaconf import DictConfig


def runDelphes(cfg : DictConfig, dir: str, run_with: str, image_name: str, logger) -> None:
    r"""Run Delphes detector simulation.
    """
    if 'block_delphes' in list(cfg['gen'].keys()):

        logger.info("Running detector simulation with Delphes.")
        if 'run_standalone' in list(cfg['gen']['block_madspin'].keys()):
            if cfg['gen']['block_madspin']['run_standalone'] == True:
                evt_dir = 'run_01_decayed_2'
            else:
                evt_dir = 'run_01_decayed_1'
        elif 'block_madspin' in list(cfg['gen'].keys()):
            evt_dir = 'run_01_decayed_1'
        else:
            evt_dir = 'run_01'

        shower = True if 'shower' in list(cfg['run'].keys()) and cfg['run']['shower'] is True else False
        file_name = glob.glob(f'{dir}/Events/{evt_dir}/*.hepmc.gz')[0] if shower else glob.glob(f'{dir}/Events/{evt_dir}/*.lhe.gz')[0]

        ecard = open(f"delphes_exec_card-{os.path.basename(dir)}","w")
        ecard.write(f"gunzip {file_name} \n")
        if shower:
            ecard.write(f"DelphesHepMC2 delphes/{cfg['gen']['block_delphes']['delphes_card']} {dir}.root {file_name[:-3]}")
        else:
            ecard.write(f"DelphesLHEF delphes/{cfg['gen']['block_delphes']['delphes_card']} {dir}.root {file_name[:-3]}")
        ecard.close()

        if run_with == "docker":
            logger.info('Running post commands using Docker.')
            subprocess.run(
                [
                    "docker", "run", "--rm", "-it", "-w", "/root",
                    "-v", f"{Path().absolute()}:/root",
                    image_name, "/bin/bash", f"delphes_exec_card-{os.path.basename(dir)}"
                ]
            )

        if run_with == "singularity":
            logger.info('Running post commands using Singularity.')
            subprocess.run(
                [
                    "singularity", "exec", "--bind", f"{Path().absolute()}",
                    image_name, "/bin/bash", f"delphes_exec_card-{os.path.basename(dir)}"
                ]
            )
