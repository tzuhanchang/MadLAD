import os

import subprocess
from pathlib import Path
from madlad.container import checkImage

from omegaconf import DictConfig


def runShower(cfg : DictConfig, dir: str, run_with: str, image_name: str, logger) -> None:
    r"""Launch parton shower for LO events.
    """
    image_name, run_with = checkImage(cfg, logger)

    logger.info('Writting LO parton shower commands.')
    evt_dir = 'run_01_decayed_1' if 'block_madspin' in list(cfg['gen'].keys()) else 'run_01'
    ecard = open(f"mg5_lo_shower_card-{os.path.basename(dir)}","w")
    ecard.write(f"launch {dir} -i\nshower {evt_dir}")
    ecard.close()

    if run_with == "docker":
        logger.info('Running parton shower for LO events using Docker.')
        subprocess.run(
            [
                "docker", "run", "--rm", "-it", "-w", "/home/atreus/data",
                "-v", f"{Path().absolute()}:/home/atreus/data",
                image_name, cfg['run']['mg5'],
                f"mg5_lo_shower_card-{os.path.basename(dir)}"
            ]
        )

    if run_with == "singularity":
        logger.info('Running parton shower for LO events using Singularity.')
        subprocess.run(
            [
                "singularity", "exec", "--bind", f"{Path().absolute()}",
                image_name, cfg['run']['mg5'],
                f"mg5_lo_shower_card-{os.path.basename(dir)}"
            ]
        )