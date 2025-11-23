Event Generation
=======================

MadLAD turns a **pre‑built container** and a single **YAML configuration file** into a full event‑generation workflow. Below is a step‑by‑step guide, the configuration syntax and an example that produces all‑hadronic \(t\bar t\) events.

---

## 1. Launching a Run

```bash
python -m madlad.generate --config-name=ttbar-allhad.yaml [options]
```

* `--config-name` – basename of the YAML file stored in `processes` folder **without** the `.yaml` extension.  
* `[options]` – optional Hydra overrides, e.g. `run.auto-launch=True`.

---

## 2. Generation Configuration

A config is split into three logical blocks:

| Block | Purpose |
|-------|---------|
| `run`  | How MadLAD should start the container (image, path to MG5, etc.). |
| `gen`  | All MadGraph‑specific options (run card, madspin, shower etc.). |
| `post` | Bash commands executed after the event generation (e.g. histogramming). |

Below is a fully commented example (`processes/ttbar-allhad.yaml`).

```yaml
# ────────────────────── run ───────────────────────
run:
  image:       "madlad-custom"            # Docker image to use
  mg5:         "/app/MG5_aMC/bin/mg5_aMC" # Path to MG5 inside the container
  launch-from: null                       # Optional: launch an existing madgraph process
  auto-launch: False                      # Whether generation should start automatically
  no-shower:   False                      # Skip parton showering

# ────────────────────── gen ───────────────────────
gen:
  # --- Model and process definition ---------------------------------
  block_model:
    model:          loop_sm-no_b_mass
    multiparticle:  ["p = g u c d s u~ c~ d~ s~ b b~",
                     "j = g u c d s u~ c~ d~ s~ b b~"]
    proc:           "p p > t t~ [QCD]"
    save_dir:       "Output"

  # --- Run card options ---------------------------------------------
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
    jetalgo:        -1          # Anti‑kT by default
    jetradius:      0.4
    ptj:            0.1
    req_acc:        0.001

  # --- MadSpin decay card -------------------------------------------
  block_madspin:
    multiparticle:  ["p = g u c d s u~ c~ d~ s~ b b~",
                     "j = g u c d s u~ c~ d~ s~ b b~"]
    decays:         ["t > w+ b, w+ > j j",
                     "t~ > w- b~, w- > j j"]
    bwcut:          15
    max_weight_ps_point: 500
    Nevents_for_max_weight: 500

  # --- Parameter card -------------------------------------------------
  block_param:
    param: "aMcAtNlo_param_card_loop_sm-no_b_mass.dat"

  # --- Custom scale definitions --------------------------------------
  block_sf:
    custom_scales: [
      "c         Q^2= mt^2 + 0.5*(pt^2+ptbar^2)",
      "          xm2=dot(pp(0,3),pp(0,3))",
      "          tmp=sqrt(xm2+0.5*(pt(pp(0,3))**2+pt(pp(0,4))**2))",
      "          temp_scale_id='mt**2 + 0.5*(pt**2+ptbar**2)'",
      ""
    ]

  # --- Delphes run card ----------------------------------------------
  block_delphes:
    delphes_card: "ATLAS_sim_FASTJET.tcl"

# ────────────────────── post ───────────────────────
post:
  - "echo 'Finished'"
```
