import hydra
import logging

from madlad.controls import makeProcess, launchEvtGen, runPost, cleanUp

from omegaconf import DictConfig


@hydra.main(version_base=None, config_path="../processes")
def Generate(cfg : DictConfig) -> None:
    logger = logging.getLogger("MadLAD")

    if cfg['run']['launch-from'] is not None:
        logger.info('A launch directory is provided, MadLAD will launch generation in this directory.')
        launchEvtGen(cfg, cfg['run']['launch-from'], logger)
    else:
        makeProcess(cfg, logger)

        if cfg['run']['auto-launch']:
            launchEvtGen(cfg, cfg['gen']['block_model']['save_dir'], logger)

    runPost(cfg, logger)

    cleanUp(cfg, logger)


if __name__ == '__main__':
    Generate()