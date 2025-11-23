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
```

For MadGraph5 (`mg5`) you can use:
* **Version** → the public release to download.  
* **Path**   → copy a local installation instead of downloading.

> **Example:** `mg5: "/opt/mg5_aMC_v2.9.18"` will copy that folder into the image.

#### 2.3 `extra`

```yaml
extra:
  pdfs:   [260000, 260400, 303400]
  models: ["2HDMtII_NLO", "HC_NLO_X0_UFO"]
```

* `pdfs` – a list of LHAPDF IDs that you want to include.
* `models` – names of MadGraph or UFO models that you want to include.
