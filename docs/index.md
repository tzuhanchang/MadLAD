<p align="center">
  <img height="150" src="_logo.png"/>
</p>

--------------------------------------------------------------------------------

**MadLAD** is a event generation wrapper built upon [MadGraph5](https://launchpad.net/mg5amcnlo)<sup>1</sup>, [Pythia8](https://pythia.org)<sup>2</sup>, [LHAPDF](https://lhapdf.hepforge.org)<sup>3</sup>, [FastJet](http://fastjet.fr)<sup>4</sup> and [Delphes](https://github.com/delphes/delphes)<sup>5</sup>. MadLAD is designed to be used with Docker or Singularity containers, which contain all necessary software and environment setups.

Contributions to this project are warmly welcomed. If you are interested in contributing, please submit a pull request with your implemented new features or fixed bugs.

- [Quick Start](#quick-start)
    - [Build your own containers](#build-your-own-containers)
    - [Generate](#generate)
    - [Reference](#reference)

## Quick Start

#### Build your own containers
```
python -m madlad.build -c examples/config_build.yaml
```
Container building require either Docker or Singularity is installed on your system.
Specifying software version you need in the build configuration file `config_build.yaml`.


#### Generate
If you want to generate events with one of our provided processes, run
```
python -m madlad.generate (--config-dir=processes/examples) --config-name=ttbar-allhad.yaml 
```
This will only produce a production directory, if you want to automatically launch the Matrix Element (ME) or Parton Shower (PS) simulation, use the option `run.auto-launch=True`. You can also define your own processes and save them to `processes` directory.


#### Reference
---
1. Alwall, Johan, et al. *"The automated computation of tree-level and next-to-leading order differential cross sections, and their matching to parton shower simulations."* Journal of High Energy Physics 2014.7 (2014): 1-157. <br>
2. Sjöstrand, Torbjörn, et al. *"An introduction to PYTHIA 8.2."* Computer physics communications 191 (2015): 159-177. <br>
3. Buckley, Andy, et al. *"LHAPDF6: parton density access in the LHC precision era."* The European Physical Journal C 75 (2015): 1-20. <br>
4. Cacciari, Matteo, Gavin P. Salam, and Gregory Soyez. *"FastJet user manual: (for version 3.0. 2)."* The European Physical Journal C 72 (2012): 1-54. <br>
5. De Favereau, J., et al. *"DELPHES 3: a modular framework for fast simulation of a generic collider experiment."* Journal of High Energy Physics 2014.2 (2014): 1-26.