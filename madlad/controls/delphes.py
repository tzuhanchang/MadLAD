import os

import subprocess
from pathlib import Path

from omegaconf import DictConfig


def runDelphes(cfg : DictConfig, dir: str, run_with: str, image_name: str, logger) -> None:
    r"""Run Delphes detector simulation.
    """
    if 'block_delphes' in list(cfg['gen'].keys()):

        logger.info("Running detector simulation with Delphes.")
        evt_dir = 'run_01_decayed_1' if 'block_madspin' in list(cfg['gen'].keys()) else 'run_01'

        shower = True if 'shower' in list(cfg['run'].keys()) and cfg['run']['shower'] is True else False
        if cfg['gen']['block_model']['order'] == "nlo" or 'order' not in list(cfg['gen']['block_model']):
            file_name = 'events_PYTHIA8_0.hepmc' if shower else 'events.lhe'
        else:
            file_name = 'tag_1_pythia8_events.hepmc' if shower else 'unweighted_events.lhe'

        ecard = open(f"delphes_exec_card-{os.path.basename(dir)}","w")
        ecard.write(f"gunzip {dir}/Events/{evt_dir}/{file_name}+'.gz' \n")
        if shower:
            ecard.write(f"DelphesHepMC2 delphes/{cfg['gen']['block_delphes']['delphes_card']} {dir}.root {dir}/Events/{evt_dir}/{file_name}")
        else:
            ecard.write(f"DelphesLHEF delphes/{cfg['gen']['block_delphes']['delphes_card']} {dir}.root {dir}/Events/{evt_dir}/{file_name}")
        ecard.close()

        if run_with == "docker":
            logger.info('Running post commands using Docker.')
            subprocess.run(
                [
                    "docker", "run", "--rm", "-it", "-w", "/home/atreus/data",
                    "-v", f"{Path().absolute()}:/home/atreus/data",
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