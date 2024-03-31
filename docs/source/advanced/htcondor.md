MadLAD + HTCondor
=======================

!!! Warning

    Running MadLAD on HTCondor requires `singularity`.

To start, you need to build a `singularity` image containing model and PDF set required for the run following [this tutorial](../tutorials/build_containers.md).
You also need a submit description file (`submit.sub`) and a run script (`job_condor.sh`). Then run

```bash
condor_submit submit.sub
```

`submit.sub` instructs HTCondor how to run the job, [learn more](https://htcondor.readthedocs.io/en/latest/users-manual/submitting-a-job.html).
The following is a simple submit description file:
```
executable              = job_condor.sh
Requirements            = HasSingularity
arguments               = $(ClusterId)$(ProcId)
output                  = $(ClusterId).$(ProcId).out
error                   = $(ClusterId).$(ProcId).err
log                     = $(ClusterId).log
environment             = "ClusterId=$(ClusterId) ProcId=$(ProcId)"
should_transfer_files   = YES
transfer_input_files    = MadLAD, job_condor.sh
when_to_transfer_output = ON_EXIT
transfer_output_files   = MadLAD/Output
request_CPUs = 8
queue 100
```
We set `Requirements = HasSingularity`, which only requests nodes with `singularity` installed.
The HTCondor job is initiated by transferring `MadLAD` folder and run script `job_condor.sh` to the node, defined in `transfer_input_files`.
On exit, `MadLAD/Output` is transferred out the node, defined in `transfer_output_files` (this should be set to the path corresponding to the `save_dir` in your process configuration file).

The executable, `job_condor.sh`, includes basic MadLAD generation commands:
```bash
#!/bin/bash

cd MadLAD   # Execute in MadLAD folder

python -m madlad.generate --config-name=ttbar-allhad.yaml [options]

cd -        # Return to condor work directory
```