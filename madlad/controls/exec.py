import os

from shutil import which
import subprocess
from pathlib import Path
from madlad.container import checkImage

from madlad.parameters import edit_madspin, edit_run, edit_scales, copy_param_card, make_process
from omegaconf import DictConfig


def makeProcess(cfg : DictConfig, logger) -> None:
    r"""Create a MadGraph process.
    """
    image_name, run_with = checkImage(cfg, logger)

    if 'block_model' not in list(cfg['gen'].keys()):
        logger.error("`block_model` must be provided!")

    logger.info('Creating MG5 process.')
    make_process(cfg)

    if run_with == "docker":
        logger.info('Creating a MG5 run directory with Docker.')
        subprocess.run(
            [
                "docker", "run", "--rm", "-it", "-w", "/home/atreus/data",
                "-v", f"{Path().absolute()}:/home/atreus/data",
                image_name, cfg['run']['mg5'],
                f"proc_card_mg5-{os.path.basename(cfg['gen']['block_model']['save_dir'])}.dat"
            ]
        )

    if run_with == "singularity":
        logger.info('Creating a MG5 run directory with Singularity.')
        subprocess.run(
            [
                "singularity", "exec", "--bind", f"{Path().absolute()}",
                image_name, cfg['run']['mg5'],
                f"proc_card_mg5-{os.path.basename(cfg['gen']['block_model']['save_dir'])}.dat"
            ]
        )

    if 'block_run' in list(cfg['gen'].keys()):
        logger.info('Editing MG5 run card.')
        edit_run(cfg)
    
    if 'block_madspin' in list(cfg['gen'].keys()):
        if 'run_standalone' in list(cfg['gen']['block_madspin'].keys()):
            if cfg['gen']['block_madspin']['run_standalone'] == True:
                logger.info('Will run madspin standalone later.')
        else:
            logger.info('Editing MG5 MadSpin card.')
            edit_madspin(cfg)

    if 'block_param' in list(cfg['gen'].keys()):
        logger.info('Copying parameter card.')
        copy_param_card(cfg)

    if 'block_sf' in list(cfg['gen'].keys()):
        logger.info('Writing custom scale factors.')
        edit_scales(cfg)