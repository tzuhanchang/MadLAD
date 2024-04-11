import os

import subprocess
from pathlib import Path

from omegaconf import DictConfig


def runDelphes(cfg : DictConfig, dir: str, run_with: str, image_name: str, logger) -> None:
    r"""Run Delphes detector simulation.
    """
    if 'block_delphes' in list(cfg['gen'].keys()):

        logger.info("Running detector simulation with Delphes.")
        ecard = open(f"delphes_exec_card-{os.path.basename(dir)}","w")
        ecard.write("gunzip Output/Events/run_01_decayed_1/events_PYTHIA8_0.hepmc.gz \n")
        ecard.write(f"DelphesHepMC2 delphes/{cfg['gen']['block_delphes']['delphes_card']} {dir}.root {dir}/Events/run_01_decayed_1/events_PYTHIA8_0.hepmc")
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