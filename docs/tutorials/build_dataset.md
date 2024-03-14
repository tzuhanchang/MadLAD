Build Your Own Containers
=======================

Since MadLAD [release v3.0](https://github.com/tzuhanchang/MadLAD/releases/tag/v3.0.0), we have introduced auto container building functionality.
You can now build a container image with easy.

To build a MadLAD image:
```
python -m madlad.build -c examples/config_build.yaml
```
This command requires `yaml`, if it is not available in your python environment, try installing it with `pip install yaml`.

`examples/config_build.yaml` is a build configuration file, it has the following structure:
```
image:
  name:    "madlad-custom"

build:
  mg5:     "2.9.18" # MG5 version, (or path to a local installation)
  pythia:  "8.301"
  lhapdf:  "6.5.0"
  fastjet: "3.4.0"
  delphes: "3.5.0"

extra:
  pdfs:   [260000, 260400, 303400]          # Additional pdf sets
  models: ["2HDMtII_NLO", "HC_NLO_X0_UFO"]  # Additional models
```

The configuration file has three blocks: `image`, `build` and `extra`.
Under the `image` block, you can define the name of the output image.
You can state your preferred software version in the `build` block.
In the `extra` block, you can provide PDFs and models you wish to include in the image.

For MadGraph, if you have a local installation and want to use it in the container, you can specify the path to a local installation in `build`.
In this way, MadLAD will not attempt to download MadGraph, but instead copying your local installation into the image.