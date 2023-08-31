import shutil

from os.path import exists
from madlad.utils import config
from typing import Optional


def copy_param_card(settings: Optional[config] = None):
    """Copy the required parameter card defined in :obj:`settings` to :obj:`process_dir`.
    
    Args:
        settings (optional: madlad.utils.config): settings.
    """
    save_dir = settings.process_dir
    settings = settings.param

    paramNameToCopy = "param/"+settings['param']

    if exists(paramNameToCopy):
        pass
    else:
        raise ValueError("Cannot find {} in param folder".format(settings['param']))
    
    paramNameDestination = save_dir+'/Cards/param_card.dat'
    shutil.copy(paramNameToCopy,paramNameDestination)