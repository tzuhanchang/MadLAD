import os

from shutil import which
import subprocess
from pathlib import Path
from madlad.container import checkImage

from omegaconf import DictConfig


def runPreLaunch(cfg : DictConfig, logger) -> None:
    r"""Launch event generation.
    """
    if 'pre-launch' in list(cfg.keys()):
        image_name, run_with = checkImage(cfg, logger)

        logger.info('Writting pre-launch commands.')
        ecard = open("pre-launch-commands","w")
        for command in cfg['pre-launch']:
            ecard.write(str(command)+'\n')
        ecard.close()

        if run_with == "docker":
            logger.info('Running pre-launch commands using Docker.')
            subprocess.run(
                [
                    "docker", "run", "--rm", "-it", "-w", "/root",
                    "-v", f"{Path().absolute()}:/root",
                    image_name, "/bin/bash", f"pre-launch-commands"
                ]
            )

        if run_with == "singularity":
            logger.info('Running pre-launch commands using Singularity.')
            subprocess.run(
                [
                    "singularity", "exec", "--bind", f"{Path().absolute()}",
                    image_name, "/bin/bash", f"pre-launch-commands"
                ]
            )


def runPost(cfg : DictConfig, logger) -> None:
    r"""Launch event generation.
    """
    if 'post' in list(cfg.keys()):
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
                    "docker", "run", "--rm", "-it", "-w", "/root",
                    "-v", f"{Path().absolute()}:/root",
                    image_name, "/bin/bash", f"post-commands"
                ]
            )

        if run_with == "singularity":
            logger.info('Running post commands using Singularity.')
            subprocess.run(
                [
                    "singularity", "exec", "--bind", f"{Path().absolute()}",
                    image_name, "/bin/bash", f"post-commands"
                ]
            )