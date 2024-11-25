import os
import glob

import subprocess
from pathlib import Path

from omegaconf import DictConfig


def runPythia(cfg : DictConfig, dir: str, run_with: str, image_name: str, logger) -> None:
    r"""Run Pythia8 Parton Shower Standalone.
    """
    if 'block_pythia' in list(cfg['gen'].keys()):

        logger.info("Running parton shower with Pythia.")
        evt_dir = 'run_01_decayed_2' if 'block_madspin' in list(cfg['gen'].keys()) else 'run_01'
        # evt_dir = 'run_01' if cfg['gen']['block_pythia']['post_madspin'] == True else 'run_01'
        # evt_dir = 'run_01_decayed_1' if cfg['gen']['block_pythia']['post_madspin'] == True else 'run_01'

        shower = True if 'shower' in list(cfg['run'].keys()) and cfg['run']['shower'] is True else False
        file_name = glob.glob(f'{dir}/Events/{evt_dir}/*.lhe.gz')

        ecard = open(f"pythia_exec_card-{os.path.basename(dir)}","w")
        if cfg['run']['shower'] is False:
            logger.info('Writing Gen card, without parton shower.')
            if cfg['gen']['block_model']['order'].lower() == "lo":
                ecard.write(f"launch {dir} -i\nshower {evt_dir}")
            else:
                ecard.write(f"launch {dir} -i\nshower {evt_dir}")
        else:
            logger.info('Parton shower has already been run with MG5 generation.')
        ecard.close()

        if run_with == "docker":
            logger.info('Running post commands using Docker.')
            subprocess.run(
            [
                "docker", "run", "--rm", "-it", "-w", "/home/atreus/data",
                "-v", f"{Path().absolute()}:/home/atreus/data",
                image_name, cfg['run']['mg5'],
                f"pythia_exec_card-{os.path.basename(dir)}"
            ]
        )

        if run_with == "singularity":
            logger.info('Running post commands using Singularity.')
            subprocess.run(
            [
                "singularity", "exec", "--bind", f"{Path().absolute()}",
                image_name, cfg['run']['mg5'],
                f"pythia_exec_card-{os.path.basename(dir)}"
            ]
        )
