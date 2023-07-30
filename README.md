### MadLAD: an aMC@NLO assistant

This code is based on the generator component of [ATLAS Athena](https://gitlab.cern.ch/atlas/athena) for performing external truth-level studies using ATLAS suggested MC modellings.

- [Quick Start](#quick-start)
- [Docker](#docker)

### Quick Start
Use a build-in process initiate a MadGraph process:
```
python3 ttbar_allhad_nlo.py
```
It creates a folder `gen/ttbar_allhad_nlo`, and modifies MadGraph cards using user defined parameters. After the process is initiated, user can start generating events by running
```
mg5_aMC gen/ttbar_allhad_nlo
```
This requires `mg5_aMC` is in your `$PATH`.

---

### Docker
We understand, setting up environment is tricky, specially if you are using a Mac. So we included a `Dockerfile`, just build it and you can start generating events. Building the docker file following
```
docker build ./ -t "madlad:v1"
``` 
Start a docker container run
```
docker run -it --rm -v /Users/jo/MCs:/mnt madlad:v1 /bin/bash
```
This mounts your directory `/Users/jo/MCs` to the `data` folder inside the container.