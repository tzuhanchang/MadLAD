import os

from shutil import which
import subprocess
from pathlib import Path
from madlad.container import checkImage

from omegaconf import DictConfig


def launchEvtGen(cfg : DictConfig, dir: str, logger) -> None:
    r"""Launch event generation.
    """
    image_name, run_with = checkImage(cfg, logger)

    ecard = open(f"mg5_exec_card-{os.path.basename(dir)}","w")
    if cfg['run']['shower']:
        logger.info('Writing Gen card, without parton shower.')
        if cfg['gen']['block_model']['order'].lower() == "lo":
            ecard.write(f"launch {dir} -i\ngenerate_events")
        else:
            ecard.write(f"launch {dir} -i\ngenerate_events -p")
    else:
        logger.info('Writing Gen card.')
        ecard.write(f"launch {dir}")
    ecard.close()

    if run_with == "docker":
        logger.info('Running MG5 event generation using Docker.')
        subprocess.run(
            [
                "docker", "run", "--rm", "-it", "-w", "/home/atreus/data",
                "-v", f"{Path().absolute()}:/home/atreus/data",
                image_name, cfg['run']['mg5'],
                f"mg5_exec_card-{os.path.basename(dir)}"
            ]
        )

    if run_with == "singularity":
        logger.info('Running MG5 event generation using Singularity.')
        subprocess.run(
            [
                "singularity", "exec", "--bind", f"{Path().absolute()}",
                image_name, cfg['run']['mg5'],
                f"mg5_exec_card-{os.path.basename(dir)}"
            ]
        )