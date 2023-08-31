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

    fcard = open('proc_card_mg5.dat','w')
    fcard.write("""%s
%s
%s
%s
"""%(
    "import model "+str(settings['model']),
    str(settings['multiparticle']),
    str(settings['proc']),
    "output "+save_dir
    ) )
    
    fcard.close()

    gen = subprocess.Popen([madgraph_path, "proc_card_mg5.dat"])
    gen.wait()

    subprocess.Popen(["rm", "proc_card_mg5.dat"])