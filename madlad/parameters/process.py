import os
import subprocess

from madlad.utils import config
from typing import Optional


def make_process(settings: Optional[config] = None, madgraph_path: Optional[str] = None):
    """Make the process defined in :obj:`settings` and save to :obj:`process_dir`.

    Args:
        settings (optional: madlad.utils.config): settings.
    """
    save_dir = settings.process_dir
    settings = settings.model

    try:
        model = "import model " + settings['model']
    except KeyError:
        raise ValueError("No MadGraph model is provided! Please define in the configuration file.")

    try:
        proc = "generate " + settings['proc']
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
"""%(
    model,
    multiparticle,
    proc,
    "output "+save_dir
    ) )

    fcard.close()

    gen = subprocess.Popen([madgraph_path, f"proc_card_mg5-{os.path.basename(save_dir)}.dat"])
    gen.wait()

    subprocess.Popen(["rm", f"proc_card_mg5-{os.path.basename(save_dir)}.dat"])
