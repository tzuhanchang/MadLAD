import fileinput

from madlad.utils import config
from typing import Optional


def edit_scales(settings: Optional[config] = None):
    r"""Use a custom dynmaical scale by editing `setscales.f` under :obj:`process_dir`/SubProcesses.

    Args:
        process_dir (optional: str): aMC process directory.
        settings (optional: madlad.utils.config): settings.
    """
    save_dir = settings.process_dir
    settings = settings.scales

    if 'custom_scales' not in list(settings.keys()):
        raise ValueError("Cannot find `custom_scales`, please provide it in config.")
    
    fileN = save_dir+'/SubProcesses/setscales.f'
    mark  = '      elseif(dynamical_scale_choice.eq.10) then'
    rmLines = ['ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc',
            'cc      USER-DEFINED SCALE: ENTER YOUR CODE HERE                                 cc',
            'cc      to use this code you must set                                            cc',
            'cc                 dynamical_scale_choice = 0                                    cc',
            'cc      in the run_card (run_card.dat)                                           cc',
            'write(*,*) "User-defined scale not set"',
            'stop 1',
            'temp_scale_id=\'User-defined dynamical scale\' ! use a meaningful string',
            'tmp = 0',
            'cc      USER-DEFINED SCALE: END OF USER CODE                                     cc'
            ]

    for line in fileinput.input(fileN, inplace=True):
        toKeep = True
        for rmLine in rmLines:
            if rmLine in line:
                toKeep = False
                break
        if toKeep:
            print(line, end="")  # Use end="" to prevent adding a newline
        if line.startswith(mark):
            for scales in settings['custom_scales']:
                print(scales)