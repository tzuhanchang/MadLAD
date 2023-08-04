from src import modify_run_card, modify_scales, modify_madspin_card
import fileinput
import shutil
import subprocess

# ttbar with all hadronic decays in next-to-leading order QCD.
proc   = 'generate p p > x0 t1 b1 j $$ w+ w- [QCD]'
wdecay = "decay t > w+ b, w+ > all all \ndecay t~ > w- b~, w- > all all \n"

CPalpha = 0 # CP mixing angle

nevents = 100000
nevt_job= 1000

beamEnergy = 6500

pdflabel='lhapdf'
lhaid   = 260400
pdfmin  = 260401
pdfmax  = 260500

reweight_scale = '.true.'
reweight_PDF   = '.true.'
parton_shower  = 'PYTHIA8'
dyn_scale      = '3'    # user-defined scale -> Dominic's definition of mt+1/2*(pt^2+ptx^2)
bwcut          = 50

process_dir = "gen/tHjb_CP_nlo"
randomSeed  = 65

# --------------------------------------------------------------
#  Proc card writing
# --------------------------------------------------------------
fcard = open('proc_card_mg5.dat','w')
fcard.write("""import model HC_NLO_X0_UFO-4Fnoyb
define p = g u c d s u~ c~ d~ s~
define j = g u c d s u~ c~ d~ s~
define t1 = t t~
define b1 = b b~
"""+proc+"""
output {}
""".format(process_dir))
fcard.close()

gen = subprocess.Popen(["mg5", "proc_card_mg5.dat"])
gen.wait()

subprocess.Popen(["rm", "proc_card_mg5.dat"])

# --------------------------------------------------------------
#  Start building the cards
# --------------------------------------------------------------
# Decay with MadSpin
modify_madspin_card(
    process_dir=process_dir,
    decays=wdecay,
    bwcut=bwcut,
    randomSeed=randomSeed
)

# --------------------------------------------------------------
#  Additional run card options
# --------------------------------------------------------------
run_card_extras = { 'lhaid'         : lhaid,
                    'pdlabel'       : "'"+pdflabel+"'",
                    'parton_shower' : parton_shower,
                    'reweight_scale': reweight_scale,
                    'reweight_PDF'  : reweight_PDF,
                    'PDF_set_min'   : pdfmin,
                    'PDF_set_max'   : pdfmax,
                    'dynamical_scale_choice' : dyn_scale,
                    'jetalgo'   : '-1',  # use anti-kT jet algorithm
                    'jetradius' : '0.4', # set jet cone size of 0.4
                    'ptj'       : '0.1', # minimum jet pT
                    'req_acc'   : '0.001',
                    'nevents'   : nevents,
                    'nevt_job'  : nevt_job,
                    'iseed'     : randomSeed,
                    'beamenergy': beamEnergy
                    }

# Run card
modify_run_card(
      process_dir = process_dir,
      settings    = run_card_extras
      )

# Param card
paramNameToCopy      = 'param/param_card_CPalpha_{}.dat'.format(CPalpha) #'aMcAtNlo_param_card_tt.dat'
paramNameDestination = process_dir+'/Cards/param_card.dat'
shutil.copy(paramNameToCopy,paramNameDestination)
