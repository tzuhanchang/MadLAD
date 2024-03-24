import yaml

from shutil import which
from omegaconf import DictConfig, OmegaConf

from madlad.container import DockerBuild, SingularityBuild


def checkImage(cfg : DictConfig, logger) -> str:
    r"""Check if required image is available on the system.
    If image is not found, MadLAD will build default image.
    """
    if not yaml.load(OmegaConf.to_yaml(cfg), Loader=yaml.SafeLoader):
        logger.error("Configuration file is not provided! \
            \nPlease place it under `processes` folder and provide it via `--config-name`.")

    if which("docker") is not None and which("singularity") is not None:
        logger.error("`Docker` and `singularity` not found on your system. \
            \nIf you think this is a mistake, please report this to https://github.com/tzuhanchang/MadLAD.")

    if cfg['run']['image'] is None or cfg['run']['image'] == "":
        logger.warning("No image is provided, MadLAD will build a default image, it may not have the models or pdfs you need. \
            \nThe run might fail! To cancel this, press CONTROL+C.")

        if which("docker"):
            DockerBuild('examples/config_build.yaml')
            image_name = "madlad-custom"
        
        elif which("singularity"):
            SingularityBuild('examples/config_build.yaml')
            image_name = "madlad-custom.sif"
    else:
        image_name = cfg['run']['image']

    return image_name