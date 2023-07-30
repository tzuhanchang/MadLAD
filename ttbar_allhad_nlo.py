from src import modify_run_card, modify_scales, modify_madspin_card
import fileinput
import shutil
import subprocess

# ttbar with all hadronic decays in next-to-leading order QCD.
proc   = 'generate p p > t t~ [QCD]'
wdecay = "decay t > w+ b, w+ > j j \ndecay t~ > w- b~, w- > j j \n"

nevents = 1000

beamEnergy = 6500

pdflabel='lhapdf'
lhaid   = 260000
pdfmin  = 260001
pdfmax  = 260100

reweight_scale = '.true.'
reweight_PDF   = '.true.'
maxjetflavor   = 5
parton_shower  = 'PYTHIA8'
muR_over_ref   = 1.0
muF1_over_ref  = 1.0
muF2_over_ref  = 1.0
dyn_scale      = '10'    # user-defined scale -> Dominic's definition of mt+1/2*(pt^2+ptx^2)
bwcut          = 15

process_dir = "gen/test_gen"
randomSeed  = 36

# --------------------------------------------------------------
#  Proc card writing
# --------------------------------------------------------------
fcard = open('proc_card_mg5.dat','w')
fcard.write("""import model loop_sm-no_b_mass
define p = g u c d s u~ c~ d~ s~ b b~
define j = g u c d s u~ c~ d~ s~ b b~
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

modify_scales(
    process_dir=process_dir,
    custom_scales="""c         Q^2= mt^2 + 0.5*(pt^2+ptbar^2)
          xm2=dot(pp(0,3),pp(0,3))
          tmp=sqrt(xm2+0.5*(pt(pp(0,3))**2+pt(pp(0,4))**2))
          temp_scale_id='mt**2 + 0.5*(pt**2+ptbar**2)'
              """
)


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
                    'maxjetflavor'  : maxjetflavor,
                    'reweight_scale': reweight_scale,
                    'reweight_PDF'  : reweight_PDF,
                    'PDF_set_min'   : pdfmin,
                    'PDF_set_max'   : pdfmax,
                    'muR_over_ref'  : muR_over_ref,
                    'muF1_over_ref' : muF1_over_ref,
                    'muF2_over_ref' : muF2_over_ref,
                    'dynamical_scale_choice' : dyn_scale,
                    'jetalgo'   : '-1',  # use anti-kT jet algorithm
                    'jetradius' : '0.4', # set jet cone size of 0.4
                    'ptj'       : '0.1', # minimum jet pT
                    'req_acc'   : '0.001',
                    'nevents'   : nevents,
                    'iseed'     : randomSeed,
                    'beamenergy': beamEnergy
                    }

# Run card
modify_run_card(
      process_dir = process_dir,
      settings    = run_card_extras
      )

# Param card
paramNameToCopy      = 'param/aMcAtNlo_param_card_loop_sm-no_b_mass.dat' #'aMcAtNlo_param_card_tt.dat'
paramNameDestination = process_dir+'/Cards/param_card.dat'
shutil.copy(paramNameToCopy,paramNameDestination)
