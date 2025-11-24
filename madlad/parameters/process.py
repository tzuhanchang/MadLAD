import os

from omegaconf import DictConfig, listconfig


def make_process(cfg : DictConfig) -> None:
    """Make the process defined in :obj:`settings` and save to :obj:`process_dir`.

    Args:
        settings (optional: madlad.utils.config): settings.
    """
    save_dir = cfg['gen']['block_model']['save_dir']
    settings = cfg['gen']['block_model']

    run_settings = ""
    if 'block_settings' in cfg['gen'].keys():
        for name, val in cfg['gen']['block_settings'].items():
            run_settings += f"set {name} {val}\n"

    try:
        model = "import model " + settings['model']
    except KeyError:
        raise ValueError("No MadGraph model is provided! Please define in the configuration file.")

    try:
        print(type(settings['proc']))
        if type(settings['proc']) == str:
            proc = f"generate {settings['proc']}"
        elif type(settings['proc']) == listconfig.ListConfig:
            proc = ""
            for i, sub_proc in enumerate(settings['proc']):
                if i == 0:
                    proc += f"generate {sub_proc}\n"
                else:
                    proc += f"add process {sub_proc}\n"
        else:
            raise ValueError("Please report this issue on GitHub")

    except KeyError:
        raise ValueError("No MadGraph process is provided! Please define in the configuration file.")

    try:
        multiparticle = ""
        for defined in settings['multiparticle']:
            multiparticle += "define " + defined + "\n"
    except KeyError:
        multiparticle = ""


    fcard = open(f"proc_card_mg5-{os.path.basename(save_dir)}.dat",'w')
    fcard.write("""%s
%s
%s
%s
%s
"""%(
    run_settings,
    model,
    multiparticle,
    proc,
    "output "+save_dir
    ) )

    fcard.close()
