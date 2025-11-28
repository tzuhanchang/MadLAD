Built-in Processes
=======================

Below you’ll find the **built‑in Monte‑Carlo (MC) processes** that ship with MadLAD. If you need something else, or want to add a new one, feel free to open an **issue** [here](https://github.com/tzuhanchang/MadLAD/issues) or a **pull request** [here](https://github.com/tzuhanchang/MadLAD/pulls).  Contributions are always welcome!  

| Category | Process | **Order** | Description | Recommendation |
|------------------|-------------------|-----|-------------------------------------------|-----------------|
| **Top quarks**   | `ttbar-allhad`    | NLO | $t\bar{t}$ → all‑hadronic                 |                 |
|                  | `ttbar-dilep`     | NLO | $t\bar{t}$ → di-leptonic                  |                 |
|                  | `ttbar-semilep`   | NLO | $t\bar{t}$ → semi-leptonic                |                 |
|                  | `4top`            | NLO | $t\bar{t}t\bar{t}$ → inclusive            |                 |
| **Higgs**        | `ggF_H_FxFx`      | NLO | ggF $H$ → inclusive (FxFx)                | MG5=v2.9.*      |
|                  | `VBF_HWW-vlvl`    | NLO | VBF $H$→$W^+W^-$→$\nu l^+ \bar{\nu} l^-$  | MG5=v2.9.*      |
| **Higgs + tops** | `ttH_nlo`         | NLO | $t\bar{t}H$ → inclusive                   |                 |
| **SM**           | `Ztautau-vvlvvl`  | NLO | $Z$→$\tau^+\tau^-$ ($\tau^\pm$→$\nu_\tau\nu_{l^\pm}l^\pm$)| |


> **Tip:** Each process name is the identifier you pass to `python -m madlad.generate --config-name=<name>`. For example:  
> ```bash
> python -m madlad.generate --config-name=ttbar-allhad
> ```

---

### How to add a new process

1. **Create the configuration** (`<name>.yaml`) in `examples/` or a dedicated folder.  
2. **Add the YAML file** to the repository (or propose it via a PR).  
3. **Tag your change** with a clear description, e.g., *“Add $t\bar{t}\gamma$ at NLO”*.  

That’s it!  The next time someone else wish to run `madlad.generate`, the new process will be available out of the box.