import os

import subprocess
from pathlib import Path
from madlad.container import checkImage
from madlad.controls import runDelphes

from omegaconf import DictConfig


def launchEvtGen(cfg : DictConfig, dir: str, logger) -> None:
    r"""Launch event generation.
    """
    image_name, run_with = checkImage(cfg, logger)

    ecard = open(f"mg5_exec_card-{os.path.basename(dir)}","w")
    if 'block_settings' in cfg['gen'].keys():
        for name, val in cfg['gen']['block_settings'].items():
            ecard.write(f"set {name} {val}\n")
    if cfg['run']['shower'] is False:
        logger.info('Writing Gen card, without parton shower.')
        if cfg['gen']['block_model']['order'].lower() == "lo":
            ecard.write(f"launch {dir} -i\ngenerate_events")
        else:
            ecard.write(f"launch {dir} -i\ngenerate_events -p")
    else:
        logger.info('Writing Gen card.')
        if cfg['gen']['block_model']['order'].lower() == "lo":
            ecard.write(f"launch {dir} \nshower=Pythia8")
        else:
            ecard.write(f"launch {dir}")
    ecard.close()

    if run_with == "docker":
        logger.info('Running MG5 event generation using Docker.')
        subprocess.run(
            [
                "docker", "run", "--rm", "-it", "-w", "/root",
                "-v", f"{Path().absolute()}:/root",
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

    runDelphes(cfg, dir, run_with, image_name, logger)
