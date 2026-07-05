Build Container
=======================

Since MadLAD [release v3.0](https://github.com/tzuhanchang/MadLAD/releases/tag/v3.0.0), we have introduced auto container building functionality.
You can now build a container image with easy.


---

### 1. Quick‑Start

```bash
python -m madlad.build -c examples/config_build.yaml
```

* `-c / --config` – path to your YAML configuration (default: `examples/config_build.yaml`).  
* The script will pull the required software, assemble the image and tag it with the name you specify.

---

### 2. Container Build Configuration

`config_build.yaml` is split into three logical blocks:

| Block | Purpose | Example |
|-------|---------|---------|
| `image` | Image metadata (name, tags) | `name: "madlad-custom"` |
| `build` | Software to include and their versions (or local paths) | See below |
| `extra` | Optional additions: PDFs, models, etc. | See below |

#### 2.1 `image`

```yaml
image:
  name: "madlad-custom" 
```

> *Optional:* With Docker, you can add a `tag:` key if you want multiple tags.

#### 2.2 `build`

```yaml
build:
  mg5:     "2.9.18"   # MadGraph version (or local path)
  pythia:  "8.301"
  lhapdf:  "6.5.0"
  fastjet: "3.4.0"
  delphes: "3.5.0"
  herwig:  "7.3.0"    # Optional: Herwig 7, for NLO (aMC@NLO) parton showering
  thepeg:  "2.3.0"    # Optional: ThePEG version paired with `herwig` (default "2.3.0")
```

For MadGraph5 (`mg5`) you can use:
* **Version** → the public release to download.  
* **Path**   → copy a local installation instead of downloading.

> **Example:** `mg5: "/opt/mg5_aMC_v2.9.18"` will copy that folder into the image.

`herwig` is optional. If omitted, no Herwig software is built and only Pythia8 is available.
If provided, MadLAD builds [ThePEG](https://thepeg.hepforge.org) and [Herwig 7](https://herwig.hepforge.org)
from source and points MG5 at them (`hwpp_path`, `thepeg_path`, `hepmc_path` in `mg5_configuration.txt`).

> **Note:** MadGraph5 only exposes a Herwig7/HerwigPP interface for **NLO (aMC@NLO)** event generation,
> selected via `parton_shower: "HERWIGPP"` in `block_run` (see [Event Generation](event-generation.md)).
> There is no on‑the‑fly Herwig interface for LO (MadEvent) generation — that path remains Pythia8‑only.
> The MC@NLO–Herwig interface itself is also not officially validated by the MG5 developers (no FxFx/merging support),
> so treat it as best‑effort.

#### 2.3 `extra`

```yaml
extra:
  pdfs:   [260000, 260400, 303400]
  models: ["2HDMtII_NLO", "HC_NLO_X0_UFO"]
```

* `pdfs` – a list of LHAPDF IDs that you want to include.
* `models` – names of MadGraph or UFO models that you want to include.
