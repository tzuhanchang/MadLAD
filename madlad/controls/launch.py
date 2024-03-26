import os

from shutil import which
import subprocess
from pathlib import Path
from madlad.container import checkImage

from omegaconf import DictConfig


def launchEvtGen(cfg : DictConfig, dir: str, logger) -> None:
    r"""Launch event generation.
    """
    image_name = checkImage(cfg, logger)

    ecard = open(f"mg5_exec_card-{os.path.basename(dir)}","w")
    if cfg['run']['no-shower']:
        logger.info('Writing Gen card, without parton shower.')
        ecard.write(f"launch {dir} -i\ngenerate_events -p")
    else:
        logger.info('Writing Gen card.')
        ecard.write(f"launch {dir}")
    ecard.close()

    if which("docker") is not None:
        logger.info('Running MG5 event generation using Docker.')
        subprocess.run(
            [
                "docker", "run", "--rm", "-it", "-w", "/home/atreus/data",
                "-v", f"{Path().absolute()}:/home/atreus/data",
                image_name, cfg['run']['mg5'],
                f"mg5_exec_card-{os.path.basename(dir)}"
            ]
        )

    elif which("singularity") is not None:
        logger.info('Running MG5 event generation using Singularity.')
        subprocess.run(
            [
                "singularity", "exec", "--bind", f"{Path().absolute()}",
                image_name, cfg['run']['mg5'],
                f"mg5_exec_card-{os.path.basename(dir)}"
            ]
        )