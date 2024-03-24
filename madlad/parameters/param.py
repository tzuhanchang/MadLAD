import shutil

from os.path import exists
from omegaconf import DictConfig


def copy_param_card(cfg: DictConfig) -> None:
    """Copy the required parameter card defined in :obj:`settings` to :obj:`process_dir`.
    
    Args:
        settings (optional: madlad.utils.config): settings.
    """
    save_dir = cfg['gen']['block_model']['save_dir']
    settings = cfg['gen']['block_param']

    paramNameToCopy = "param/"+settings['param']

    if exists(paramNameToCopy):
        pass
    else:
        raise ValueError("Cannot find {} in param folder".format(settings['param']))
    
    paramNameDestination = save_dir+'/Cards/param_card.dat'
    shutil.copy(paramNameToCopy,paramNameDestination)