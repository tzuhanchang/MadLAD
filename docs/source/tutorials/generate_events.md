Generate Events
=======================

Generate events with MadLAD is simple, all you need are:

 * A pre-built MadLAD image (see [here](build_containers.md))
 * A configuration file


A configuration file contains necessary information for the generation, such as the model, physics process and center-of-mass energy, etc.
In this tutorial, we will use ttbar events with all-hadronic final states as an example, whose configuration file can be found in `processes/ttbar-allhad.yaml`.

``` yaml
run:
  image:       "madlad-custom"
  mg5:         "/app/MG5_aMC/bin/mg5_aMC"
  launch-from: null
  auto-launch: False
  no-shower:   False

gen:
  block_model:
    model:          loop_sm-no_b_mass
    multiparticle:  ["p = g u c d s u~ c~ d~ s~ b b~", "j = g u c d s u~ c~ d~ s~ b b~"]
    proc:           "p p > t t~ [QCD]"
    save_dir:       "Output"

  block_run:
    nevents:        1000
    nevt_job:       1000
    iseed:          0
    beamenergy:     6500
    pdlabel:        "lhapdf"
    lhaid:          260000
    parton_shower:  "PYTHIA8"
    maxjetflavor:   5
    reweight_scale: ".true."
    reweight_PDF:   ".true."
    PDF_set_min:    260001
    PDF_set_max:    260100
    muR_over_ref:   1.0
    muF1_over_ref:  1.0
    muF2_over_ref:  1.0
    dynamical_scale_choice: 10
    jetalgo:        -1
    jetradius:      0.4
    ptj:            0.1
    req_acc:        0.001
  
  block_madspin:
    multiparticle:  ["p = g u c d s u~ c~ d~ s~ b b~", "j = g u c d s u~ c~ d~ s~ b b~"]
    decays:         ["t > w+ b, w+ > j j", "t~ > w- b~, w- > j j"]
    bwcut:          15
    max_weight_ps_point: 500
    Nevents_for_max_weight: 500

  block_param:
    param: "aMcAtNlo_param_card_loop_sm-no_b_mass.dat"

  block_sf:
    custom_scales: [
        "c         Q^2= mt^2 + 0.5*(pt^2+ptbar^2)",
        "          xm2=dot(pp(0,3),pp(0,3))",
        "          tmp=sqrt(xm2+0.5*(pt(pp(0,3))**2+pt(pp(0,4))**2))",
        "          temp_scale_id='mt**2 + 0.5*(pt**2+ptbar**2)'",
        "              "
    ]

post: [
  "echo 'Finished'"
]
```

In this configuration file, there are three sections: `run`, `gen` and `post`.
Configures in `run` controls how MadLAD launch MadGraph.
`gen` contains various control blocks: `block_model`, `block_run`, `block_madspin`, `block_param` and `block_sf`, they are used to overwrite correponding options in different MadGraph's `Cards`.
Finally, `post` is a list of `bash` commands that tells what MadLAD should execute after event generation, such as running Delphes detector simulation.

!!! Note

    Any custom configuration file must be place in `processes` folder.


To generate events, run
```
python -m madlad.generate --config-name=ttbar-allhad.yaml [options]
```
MadLAD uses [hydra](https://hydra.cc) for configuring run ([#23](https://github.com/tzuhanchang/MadLAD/pull/23)). You can overwrite any option using, for example `run.auto-launch=True` at the end, it overwrites the `auto-launch` option provided in your configuration file.