HTCondor
=======================

!!! Warning

    Running MadLAD on HTCondor requires `singularity`.

To start, you need to build a `singularity` image containing model and PDF set required for the run following [this tutorial](../get-started/build-container.md).
You also need a submit description file (`submit.sub`) and an executable (`job_condor.sh`). Submitting job to HTCondor, run:

---

## 1. Overview

The workflow consists of three parts:

| Step | What you need | Why |
|------|---------------|-----|
| 1️⃣ Build a Singularity image | `singularity build` (see the container‑build tutorial) | The image contains all of MadLAD’s dependencies, your UFO models and PDF sets. |
| 2️⃣ Create a Condor submit description (`submit.sub`) | A small text file that tells HTCondor how to run the job | Specifies the executable, resources and file transfer rules. |
| 3️⃣ Write an executable (`job_condor.sh`) | A Bash wrapper that activates your Conda environment and runs MadLAD | Keeps the Condor job simple – it just calls a script. |

Once those pieces are in place you can submit the job with:

```bash
condor_submit submit.sub
```

---

## 2. Building the Singularity Image

Follow the [this guide](../get-started/build-container.md) to create a Singularity image that contains:

- MadLAD itself
- The UFO model(s) you want to use
- Any PDF sets that your processes require

> **Tip** – Keep the image lightweight: only add what you actually need for your workflow.

---

## 3. HTCondor Submit Description (`submit.sub`)

Below is a minimal but complete submit file that you can copy into your project directory. Feel free to tweak the resource requests (`request_CPUs`, `queue`) to match your workload.

```text
# submit.sub – HTCondor job description for MadLAD

executable              = job_condor.sh
Requirements            = HasSingularity          # Only use nodes that have Singularity
arguments               = $(ClusterId)$(ProcId)
output                  = $(ClusterId).$(ProcId).out
error                   = $(ClusterId).$(ProcId).err
log                     = $(ClusterId).log
environment             = "ClusterId=$(ClusterId) ProcId=$(ProcId)"
should_transfer_files   = YES
transfer_input_files    = MadLAD, job_condor.sh  # Transfer the code and wrapper
when_to_transfer_output = ON_EXIT
transfer_output_files   = MadLAD/Output          # Path must match `save_dir` in config
request_CPUs = 8                                 # Adjust to your job’s CPU needs
queue 100                                        # Submit 100 parallel jobs
```

### What each directive does

| Directive | Meaning |
|-----------|---------|
| `executable` | The script that Condor will run on the worker node |
| `Requirements` | Ensures the node has Singularity (`HasSingularity`) |
| `arguments` | Passes a unique ID to the script (you can use it in logs or filenames) |
| `output`, `error` | Where stdout and stderr will be written on the submit machine |
| `log` | Condor’s internal job log (not your output) |
| `environment` | Passes variables into the wrapper script |
| `transfer_input_files` | Files that need to be copied to the worker node before execution |
| `when_to_transfer_output` | When to copy results back (`ON_EXIT` is usually what you want) |
| `transfer_output_files` | Where the output of your job lives – make sure it matches the path you set in MadLAD’s `save_dir` |
| `request_CPUs` | Number of CPU cores requested for the job |
| `queue` | How many jobs to submit |

---

## 4. The Condor Executable (`job_condor.sh`)

```bash
#!/bin/bash

# ------------------------------------------------------------------
# 1. Activate the environment that contains MadLAD and dependencies
# ------------------------------------------------------------------
source /opt/miniconda3/etc/profile.d/conda.sh   # Adjust if Miniconda lives elsewhere
conda activate madlad

# ------------------------------------------------------------------
# 2. Compute a unique random seed for this job
#    -----------------------------------------
#    ClusterId and ProcId are supplied by HTCondor.
#    The constant 639945 is the first job number you submit in this
#    workflow – change it if you start a fresh batch at a different
#    ClusterId.  The arithmetic is just a quick, reproducible way to
#    generate a large range of seeds without collisions.
# ------------------------------------------------------------------
seed=$(((ClusterId + ProcId - 639945) * 30000 + 390 * 10))
echo "Random seed is set to $seed."

# ------------------------------------------------------------------
# 3. Change into the folder that Condor transferred
# ------------------------------------------------------------------
cd MadLAD   # The directory you specified in transfer_input_files

# ------------------------------------------------------------------
# 4. Run MadLAD with the user‑supplied configuration
#    -----------------------------------------------
#    * --config-name  → your YAML config (e.g. ttbar-allhad.yaml)
#    * run.image     → the name of your Singularity image
#    * gen.block_settings.nb_core   → CPU cores you want to use
#    * gen.block_run.nevents        → number of events per job
#    * gen.block_run.iseed          → the seed we just computed
# ------------------------------------------------------------------
python -m madlad.generate \
  --config-name=ttbar-allhad.yaml \
  run.image=madlad-custom \
  gen.block_settings.nb_core=4 \
  gen.block_model.save_dir=test_ttbar \
  gen.block_run.nevents=100000 \
  gen.block_run.iseed=$seed

# ------------------------------------------------------------------
# 5. Return to the Condor working directory
#    (optional – just a tidy‑up)
# ------------------------------------------------------------------
cd -
```

!!! Warning

    Change the random seeds for different Condor jobs, otherwise you will ended up with same set of events.
    e.g. **`gen.block_run.iseed=$((ClusterId + ProcId - first_cluster) * 30000 + 3900)`**


---

## 5. Submitting and Monitoring

```bash
# Submit the job
condor_submit submit.sub

# Check status
condor_q   # Show your jobs in the queue

# View logs
cat $(ClusterId).$(ProcId).out   # Stdout of the job
cat $(ClusterId).$(ProcId).err   # Stderr (error messages)
```
