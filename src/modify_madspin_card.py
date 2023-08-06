def modify_madspin_card(process_dir: str = None, decays: str = "", bwcut: int = 15, 
                        max_weight_ps_point: int = 500, Nevents_for_max_weight: int = 500,
                        randomSeed: int = 1):
    madspin_card_loc=process_dir+'/Cards/madspin_card.dat'
    mscard = open(madspin_card_loc,'w')
    mscard.write("""#************************************************************
#*                        MadSpin                           *
#*                                                          *
#*    P. Artoisenet, R. Frederix, R. Rietkerk, O. Mattelaer *
#*                                                          *
#*    Part of the MadGraph5_aMC@NLO Framework:              *
#*    The MadGraph5_aMC@NLO Development Team - Find us at   *
#*    https://server06.fynu.ucl.ac.be/projects/madgraph     *
#*                                                          *
#************************************************************
set max_weight_ps_point %i  # number of PS to estimate the maximum for each event
set Nevents_for_max_weight %i
set BW_cut %i
set seed %i
%s
launch
"""%(max_weight_ps_point, Nevents_for_max_weight, bwcut, randomSeed, decays))
    mscard.close()
