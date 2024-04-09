import os

import subprocess
from pathlib import Path
from madlad.container import checkImage

from omegaconf import DictConfig


def runPost(cfg : DictConfig, logger) -> None:
    r"""Launch event generation.
    """
    if 'post' in list(cfg.keys()):
        NUM_CPUS = 1024     # Singularity default
        if os.environ.get('OMP_NUM_THREADS') is not None:
            NUM_CPUS = os.environ.get('OMP_NUM_THREADS')

        image_name, run_with = checkImage(cfg, logger)

        logger.info('Writting post commands.')
        ecard = open("post-commands","w")
        for command in cfg['post']:
            ecard.write(str(command)+'\n')
        ecard.close()

        if run_with == "docker":
            logger.info('Running post commands using Docker.')
            subprocess.run(
                [
                    "docker", "run", "--rm", "-it", "-w", "/home/atreus/data",
                    "-v", f"{Path().absolute()}:/home/atreus/data",
                    image_name, "/bin/bash", f"post-commands"
                ]
            )

        if run_with == "singularity":
            logger.info('Running post commands using Singularity.')
            subprocess.run(
                [
                    "singularity", "exec", "--cpus", NUM_CPUS, "--bind", f"{Path().absolute()}",
                    image_name, "/bin/bash", f"post-commands"
                ]
            )