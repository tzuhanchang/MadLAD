import os
import subprocess

from omegaconf import DictConfig

def cleanUp(cfg : DictConfig, logger) -> None:

    logger.info("Running clean up.")

    if os.path.exists(f"proc_card_mg5-{os.path.basename(cfg['gen']['block_model']['save_dir'])}.dat"):
        subprocess.Popen(["rm", f"proc_card_mg5-{os.path.basename(cfg['gen']['block_model']['save_dir'])}.dat"])

    if os.path.exists(f"mg5_exec_card-{os.path.basename(cfg['gen']['block_model']['save_dir'])}"):
        subprocess.Popen(["rm", f"mg5_exec_card-{os.path.basename(cfg['gen']['block_model']['save_dir'])}"])

    if os.path.exists(f"delphes_exec_card-{os.path.basename(cfg['gen']['block_model']['save_dir'])}"):
        subprocess.Popen(["rm", f"delphes_exec_card-{os.path.basename(cfg['gen']['block_model']['save_dir'])}"])

    if os.path.exists("post-commands"):
        subprocess.Popen(["rm", "post-commands"])

    if os.path.exists("py.py"):
        subprocess.Popen(["rm", "py.py"])