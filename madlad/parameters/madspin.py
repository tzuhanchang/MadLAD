import os

from omegaconf import DictConfig


def edit_madspin(cfg: DictConfig) -> None:
    r"""Edit `madspin_card.dat` under the MadGraph process path :obj:`process_dir`.

    Args:
        process_dir (optional: str): aMC process directory.
        settings (optional: madlad.utils.config): settings.
    """
    save_dir = cfg['gen']['block_model']['save_dir']
    settings = cfg['gen']['block_madspin']

    if 'decays' not in list(settings.keys()):
        raise ValueError("Cannot find decays, please provide them in the config!")
    
    madspin_card_loc = os.path.join(save_dir, "Cards", "madspin_card.dat")
    mscard = open(madspin_card_loc,'w')

    try:
        seed = "set seed %s"%(str(settings['randomSeed']))
    except KeyError:
        seed = "# set seed 1"

    try:
        Nevents_for_max_weight = "set Nevents_for_max_weight %s # number of events for the estimate of the max. weight"%(str(settings['Nevents_for_max_weight']))
    except KeyError:
        Nevents_for_max_weight = "# set Nevents_for_max_weight 75 # number of events for the estimate of the max. weight"

    try:
        BW_cut = "set BW_cut %s                 # cut on how far the particle can be off-shell"%(str(settings['bwcut']))
    except KeyError:
        BW_cut = "# set BW_cut 15                 # cut on how far the particle can be off-shell"

    try:
        spinmode = "set spinmode %s          # Use one of the madspin special mode"%(str(settings['spinmode']))
    except KeyError:
        spinmode = "# set spinmode onshell          # Use one of the madspin special mode"

    try:
        max_weight_ps_point = "set max_weight_ps_point %s  # number of PS to estimate the maximum for each event"%(str(settings['max_weight_ps_point']))
    except KeyError:
        max_weight_ps_point = "set max_weight_ps_point 400  # number of PS to estimate the maximum for each event"

    try:
        multiparticle = ""
        for defined in settings['multiparticle']:
            multiparticle += "define " + defined + "\n"
    except KeyError:
        multiparticle = ""

    try:
        decays = ""
        for defined in settings['decays']:
            decays += "decay " + defined + "\n"
    except KeyError:
        decays = ""


    mscard.write("""#************************************************************
#*                        MadSpin                           *
#*                                                          *
#*    P. Artoisenet, R. Frederix, R. Rietkerk, O. Mattelaer * 
#*                                                          *
#*    Part of the MadGraph5_aMC@NLO Framework:              *
#*    The MadGraph5_aMC@NLO Development Team - Find us at   *
#*    https://server06.fynu.ucl.ac.be/projects/madgraph     *
#*                                                          *
#*    Manual:                                               *
#*    cp3.irmp.ucl.ac.be/projects/madgraph/wiki/MadSpin     *
#*                                                          *
#************************************************************
#Some options (uncomment to apply)
#
%s
%s
%s
%s
%s

# specify the decay for the final state particles
%s
%s
# running the actual code
launch
"""%(seed,
     Nevents_for_max_weight,
     BW_cut,
     spinmode,
     max_weight_ps_point,
     multiparticle,
     decays
    )
)
    mscard.close()