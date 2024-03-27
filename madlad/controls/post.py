import os

from shutil import which
import subprocess
from pathlib import Path
from madlad.container import checkImage

from omegaconf import DictConfig


def runPost(cfg : DictConfig, logger) -> None:
    r"""Launch event generation.
    """
    if 'post' in list(cfg.keys()):
        image_name = checkImage(cfg, logger)

        logger.info('Writting post commands.')
        ecard = open("post-commands","w")
        for command in cfg['post']:
            ecard.write(str(command)+'\n')
        ecard.close()

        if which("docker") is not None:
            logger.info('Running post commands using Docker.')
            subprocess.run(
                [
                    "docker", "run", "--rm", "-it", "-w", "/home/atreus/data",
                    "-v", f"{Path().absolute()}:/home/atreus/data",
                    image_name, "/bin/bash", f"post-commands"
                ]
            )

        elif which("singularity") is not None:
            logger.info('Running post commands using Singularity.')
            subprocess.run(
                [
                    "singularity", "exec", "--bind", f"{Path().absolute()}",
                    image_name, "/bin/bash", f"post-commands"
                ]
            )