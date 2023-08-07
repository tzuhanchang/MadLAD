#!/bin/bash

singularity exec --no-home --bind $PWD:/mnt madlad.sif bash /mnt/run_batch

