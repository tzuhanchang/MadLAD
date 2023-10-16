Container
============

**MadLAD** is designed to use inside a container to preserve consistency of generator environment and simplify the most frustrating MC generation: *get-it-to-work*. MadLAD supports [Docker](https://www.docker.com) and [Singularity](https://docs.sylabs.io/guides/3.5/user-guide/introduction.html). The later is installed on most server.

- [Docker](#docker)
- [Singularity](#singularity)

Docker
-----------

A ready-to-use Docker image is pre-build, to get the image
```
docker pull tzuhanchang/madlad:amd64
```

In this defult image, pre-installed softwares are list below
| Software      | Version       |
| ------------- | :-----------: |
| CMake         | 3.27.0        |
| ROOT          | 6.24.08       |
| Python        | 3.9.17        |
| Delphes       | 3.5.0         |
| HepMC2        | 2.06.09       |
| Pythia8       | 8.3.06        |
| Fastjet       | 3.4.0         |
| MadGraph5     | 2.9.16 LTS    |

Optionally, users can choose to build their own Docker image with additional softwares or different versions of MG5 basing on the provided `Dockerfile`.

Singularity
-----------

Using `BuildSIF.py`, a Singularity image `madlad.sif` is automatically built base on the default Docker repository (`tzuhanchang/madlad:amd64`):
```
python3 Generate.py -c processes/process_name.json
```
By including `-c processes/process_name.json` It will also download and install MG5 required model and PDF set. If you want to change the Docker repository which the Singularity image is based on, use `-r [docker-repo-name]` option.