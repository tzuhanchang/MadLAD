Generate
============

- [Define a Process](#define-a-process)
- [Generating](#generating)

Define a Process
-----------

`Generate.py` read a `.json` format process file. There are several pre-defined process files located in `./processes` aligned with ATLAS physics modeling.

There are five defination blocks: process, run parameters, mad-spin, particle parameters and custom scale function. An example of what to include is shown in `./processes/ttbar_allhad_nlo.json`:
```
[
    {
        "model": "loop_sm-no_b_mass",
        "multiparticle": [
            "p = g u c d s u~ c~ d~ s~ b b~",
            "j = g u c d s u~ c~ d~ s~ b b~"
        ],
        "proc": "p p > t t~ [QCD]",
        "save_dir": "gen/ttbar_allhad_nlo"
    },

    {
        "nevents": 100000,
        "nevt_job": 1000,
        "iseed": 0,
        "beamenergy": 6500,
        "pdlabel": "'lhapdf'",
        "lhaid": 260000,
        "parton_shower": "PYTHIA8",
        "maxjetflavor": 5,
        "reweight_scale": ".true.",
        "reweight_PDF": ".true.",
        "PDF_set_min": 260001,
        "PDF_set_max": 260100,
        "muR_over_ref": 1.0,
        "muF1_over_ref": 1.0,
        "muF2_over_ref": 1.0,
        "dynamical_scale_choice": "10",
        "jetalgo": "-1",
        "jetradius": "0.4",
        "ptj": "0.1",
        "req_acc": "0.001"
    },

    {
        "multiparticle": [
            "p = g u c d s u~ c~ d~ s~ b b~",
            "j = g u c d s u~ c~ d~ s~ b b~"
        ],
        "decays": [
            "t > w+ b, w+ > j j",
            "t~ > w- b~, w- > j j"
        ],
        "bwcut": 15,
        "max_weight_ps_point": 500,
        "Nevents_for_max_weight": 500
    },
    
    {
        "param": "aMcAtNlo_param_card_loop_sm-no_b_mass.dat"
    },

    {
        "custom_scales": [
            "c         Q^2= mt^2 + 0.5*(pt^2+ptbar^2)",
            "          xm2=dot(pp(0,3),pp(0,3))",
            "          tmp=sqrt(xm2+0.5*(pt(pp(0,3))**2+pt(pp(0,4))**2))",
            "          temp_scale_id='mt**2 + 0.5*(pt**2+ptbar**2)'",
            "              "
        ]
    }
]
```

MadLAD edits MG5 `run_card.dat`, `madspin_card.dat` and `setscales.f` automatically, and at the same time copy defined particle parameters (`param`) card saved in `./param` folder to the MG5.


Generating
-----------

**If you are already inside of a Docker container:**

you can start generating events with your process
```
python3 Generate.py -c processes/ttbar_allhad_nlo.json
```

By default, this only produces MG5 run directory (defined in config as `save_dir`), but the actual generation is not initiated. To automatically launch the generation, use `--auto_launch` option. If you want to launch from an existing run directory (called `saved_dir`), use `--launch_from saved_dir` option.


**If you are using Singularity:**

you can start by building required Singularity image according to [this guide](./container.md). Create a bash file (e.g. `exec.sh`) in the MadLAD directory
```
cd /mnt
python3 Generate.py -c processes/ttbar_allhad_nlo.json
...
```
and execute this bash file inside the Singularity container
```
singularity exec --no-home --bind $PWD:/mnt madlad.sif bash /mnt/exec.sh
``` 

Note: we mount the MadLAD directory to `/mnt` folder inside the Singularity container. Alternatively, instead of `singularity exec`, users can use `singularity shell`, which is similar to `docker run`.