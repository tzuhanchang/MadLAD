import os

from shutil import which
import subprocess
from pathlib import Path
from madlad.container import checkImage

from omegaconf import DictConfig


def runPost(cfg : DictConfig, logger) -> None:
    r"""Launch event generation.
    """
    
    run_post = False 
    
    if 'post' in list(cfg.keys()):
        run_post = True
        logger.info('Writting post commands.')
        ecard = open("post-commands","w")
        for command in cfg['post']:
            ecard.write(str(command)+'\n')
        ecard.close()
        
    
    if 'delphes' in list(cfg['run'].keys()):
        if cfg['run']['delphes'] == 'atlas':
            run_post = True
            logger.info('Writing automatic DELPHES commands to post commands')
            ecard = open("post-commands","a")
            ecard.write("gunzip Output/Events/run_01_decayed_1/events_PYTHIA8_0.hepmc.gz \n")
            delphes_command = "DelphesHepMC2 delphes/ATLAS_sim_FASTJET.tcl delphes_output.root Output/Events/run_01_decayed_1/events_PYTHIA8_0.hepmc"
            ecard.write(f"{delphes_command} \n")
            ecard.close()
        
    if run_post:
        image_name, run_with = checkImage(cfg, logger)

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
                    "singularity", "exec", "--bind", f"{Path().absolute()}",
                    image_name, "/bin/bash", f"post-commands"
                ]
            )