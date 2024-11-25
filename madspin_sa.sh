#************************************************************
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
# set seed 1

import gen/gen_name/Events/run_01/unweighted_events.lhe.gz


set Nevents_for_max_weight 75 # number of events for the estimate of the max. weight
set BW_cut 15                 # cut on how far the particle can be off-shell
# set spinmode onshell          # Use one of the madspin special mode
set max_weight_ps_point 400  # number of PS to estimate the maximum for each event
set ms_dir gen/gen_name/Events/run_01_decayed_1/ # directory where the decayed events will be stored

# specify the decay for the final state particles
define p = g u c d s b u~ c~ d~ s~ b~
define j = g u c d s b u~ c~ d~ s~ b~

# decay w+ > l+ vl
# decay w- > l- vl~
# decay z > l+ l-
decay w+ > e+ ve
decay w- > mu- vm~
decay z > mu+ mu-

# running the actual code
launch