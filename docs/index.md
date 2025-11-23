# 🎉 Welcome to **MadLAD**  

<p align="center">
  <img height="150" src="_logo.png"/>
</p>

**An all‑in‑one event‑generation wrapper for particle physics.**

MadLAD orchestrates the full chain from matrix‑element (ME) calculation to detector simulation.  
It is built on top of the following well‑known tools: [MadGraph5](https://launchpad.net/mg5amcnlo)<sup>1</sup>, [Pythia8](https://pythia.org)<sup>2</sup>, [LHAPDF](https://lhapdf.hepforge.org)<sup>3</sup>, [FastJet](http://fastjet.fr)<sup>4</sup> and [Delphes](https://github.com/delphes/delphes)<sup>5</sup>. All of these components are built into Docker or Singularity containers, so you can run MadLAD on any machine that supports one of those container runtimes.

> **Contributing** – We love community input!  
> If you’d like to add a new process, improve documentation, or fix a bug, just fork the repo and submit a pull request.

---

## 🚀 Quick Start

### 1️⃣ Build a Container

```bash
python -m madlad.build -c examples/config_build.yaml
```

*Requires Docker or Singularity to be installed.*  
The `config_build.yaml` file lets you pin the exact software versions you need.

---

### 2️⃣ Generate Events

```bash
python -m madlad.generate --config-name=ttbar-allhad
```

Feel free to drop your own process YAML files into the `processes/` directory and use them in the same way.

---

## 📚 References

| # | Citation |
|---|----------|
| 1 | J. Alwall *et al.*, “The automated computation of tree-level and next-to-leading order differential cross sections, and their matching to parton shower simulations,” *JHEP* 1407:1‑157 (2014). |
| 2 | T. Sjöstrand *et al.*, “An introduction to PYTHIA 8.2,” *Comput. Phys. Commun.* 191 (2015) 159‑177. |
| 3 | A. Buckley *et al.*, “LHAPDF6: parton density access in the LHC precision era,” *Eur. Phys. J.* C75 (2015) 1‑20. |
| 4 | M. Cacciari, G.P. Salam & G. Soyez, “FastJet user manual: (for version 3.0.2),” *Eur. Phys. J.* C72 (2012) 1‑54. |
| 5 | J. de Favereau *et al.*, “DELPHES 3: a modular framework for fast simulation of a generic collider experiment,” *JHEP* 1402 (2014) 1‑26. |

---  