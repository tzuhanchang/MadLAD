# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
 - Add `pre-launch` option ([#76](https://github.com/tzuhanchang/MadLAD/pull/76))
 - Add `ttbar-dilep` and `ttbar-semilep` processes ([#74](https://github.com/tzuhanchang/MadLAD/pull/74))
 - Add Shower Controls ([#61](https://github.com/tzuhanchang/MadLAD/pull/61))

### Changed
 - Use GitHub Page for documentation hosting ([#72](https://github.com/tzuhanchang/MadLAD/pull/72))
 - Use MkDocs Material for documentation ([#71](https://github.com/tzuhanchang/MadLAD/pull/71))

### Removed

### Fixed
 - Fix Singularity build with an external MG5 directory ([#70](https://github.com/tzuhanchang/MadLAD/pull/70))


## [v3.1.0] - 2025-05-28

### Added
 - Add LICENCE ([#66](https://github.com/tzuhanchang/MadLAD/pull/66))
 - Add options to overwrite MG5 configuration ([#65](https://github.com/tzuhanchang/MadLAD/pull/65))

### Changed
 - Change MadLAD base image to Ubuntu:20.04 ([#63](https://github.com/tzuhanchang/MadLAD/pull/63))

### Fixed
 - Fix missing line break while passing `gen.run_settings` ([#68](https://github.com/tzuhanchang/MadLAD/pull/68))
 - Fix scale writer for newer MG5 versions ([#67](https://github.com/tzuhanchang/MadLAD/pull/67))
 - Fix LO shower ([#59](https://github.com/tzuhanchang/MadLAD/pull/59))
 - Fix Singularity build with a local mg5 installation ([#56](https://github.com/tzuhanchang/MadLAD/pull/56))



## [v3.0.1] - 2024-07-08

### Added
 - Implement parton shower for LO events ([#52](https://github.com/tzuhanchang/MadLAD/pull/52))
 - Add automatic Delphes execution ([#49](https://github.com/tzuhanchang/MadLAD/pull/49))
 - Add SM 4top process ([#42](https://github.com/tzuhanchang/MadLAD/pull/42))
 - Add `Processes` documentation ([#36](https://github.com/tzuhanchang/MadLAD/pull/36))
 - Add `HTCondor` documentation ([#35](https://github.com/tzuhanchang/MadLAD/pull/35))
 - Add `order` option ([#34](https://github.com/tzuhanchang/MadLAD/pull/34))
 - Implement `post` ([#33](https://github.com/tzuhanchang/MadLAD/pull/33))
 - Add readthedocs support ([#22](https://github.com/tzuhanchang/MadLAD/pull/22))

### Changed
 - Change `no-shower` to `shower` ([#45](https://github.com/tzuhanchang/MadLAD/pull/45))
 - Use `subprocess.run` ([#27](https://github.com/tzuhanchang/MadLAD/pull/27))
 - Update `docs` following #23 ([#26](https://github.com/tzuhanchang/MadLAD/pull/26))
 - Update `madlad/__init__.py` ([#24](https://github.com/tzuhanchang/MadLAD/pull/24))
 - Use `Hydra` framework ([#23](https://github.com/tzuhanchang/MadLAD/pull/23))

### Fixed
 - Fix PDF and model download for `Docker` ([#54](https://github.com/tzuhanchang/MadLAD/pull/54))
 - Fix `gunzip` path ([#51](https://github.com/tzuhanchang/MadLAD/pull/51))
 - Fix `FileNotFoundError` ([#50](https://github.com/tzuhanchang/MadLAD/pull/50))
 - Fix `.sif` image finding ([#47](https://github.com/tzuhanchang/MadLAD/pull/47))
 - Fix MG5 build bug when use singularity ([#41](https://github.com/tzuhanchang/MadLAD/pull/41))
 - Fix missing indentation ([#40](https://github.com/tzuhanchang/MadLAD/pull/40))
 - Fix `order` query  ([#39](https://github.com/tzuhanchang/MadLAD/pull/39))
 - Fix error occurred when `docker` and `singularity` both exist ([#38](https://github.com/tzuhanchang/MadLAD/pull/38))
 - Fix `singularity` build issue ([#32](https://github.com/tzuhanchang/MadLAD/pull/32))
 - Fix `singularity` build issue ([#30](https://github.com/tzuhanchang/MadLAD/pull/30))


## [v3.0.0] - 2024-03-13

### Added
 - Add auto `singularity` build functionality ([#19](https://github.com/tzuhanchang/MadLAD/pull/19))
 - Add `CODEOWNERS` file ([#18](https://github.com/tzuhanchang/MadLAD/pull/18))
 - Add auto container building functionality ([#15](https://github.com/tzuhanchang/MadLAD/pull/15))

### Changed
 - Update `README.md` ([#21](https://github.com/tzuhanchang/MadLAD/pull/21))
 - Relocate generate commands ([#17](https://github.com/tzuhanchang/MadLAD/pull/17))
 - Move `container.py` to `madlad.container` ([#16](https://github.com/tzuhanchang/MadLAD/pull/16))


[v3.1.0]: https://github.com/tzuhanchang/MadLAD/compare/v3.0.1...v3.1.0
[v3.0.1]: https://github.com/tzuhanchang/MadLAD/compare/v3.0.0...v3.0.1
[v3.0.0]: https://github.com/tzuhanchang/MadLAD/compare/v2.0.0...v3.0.0
