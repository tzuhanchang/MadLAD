<p align="center">
  <img height="150" src=".github/logo/madlad_logo.png"/>
</p>

--------------------------------------------------------------------------------

**MadLAD** is a event generation wrapper built upon [MadGraph5](https://launchpad.net/mg5amcnlo), [Pythia8](https://pythia.org) and [Delphes](https://github.com/delphes/delphes). MadLAD is designed to be used with Docker or Singularity containers, which contain all necessary software and environment setups.

MadLAD is currently a personal project, contributions to this project are warmly welcomed. If you are interested in contributing, please submit a pull request with your implemented new features or fixed bugs.

- [Quick Start](#quick-start)
- [Generate](#generate)

### Quick Start
Get the MadLAD container from Docker:
```
docker pull tzuhanchang/madlad:amd64
```
If you are using LXPLUS, or machines with Singularity enabled, run
```
python3 BuildSIF.py -c processes/ttbar_allhad_nlo.json
```
before running generation.

---

### Generate
If you want to generate processes defined in one of the presets, make sure you are inside the container and run
```
python3 Generate.py -c processes/ttbar_allhad_nlo.json
```
This will only produce a production directory, if you want to automatically launch the Matrix Element (ME) or Parton Shower (PS) simulation, use the option ```--auto_launch```. You can also define your own processes and save them to ```.json``` files.