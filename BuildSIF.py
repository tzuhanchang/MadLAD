import argparse

from shutil import which

from madlad.utils import config, build_sif

def argparser():
    parser = argparse.ArgumentParser(description='Run event generation')
    parser.add_argument('-c', '--config', type=str,  required=True, 
                        help='Configuration/settings file.')
    parser.add_argument('-r', '--repo',   type=str,  required=False,
                        default="tzuhanchang/madlad:amd64",
                        help='The base Docker image repository.')
    return parser.parse_args()


if __name__ == '__main__':
    args = argparser()

    settings = config(args.config)

    if which("singularity") != "":
        build_sif(settings.run['lhaid'],settings.model['model'],args.repo)
    else:
        raise RuntimeError("Singularity is not detected on your system.")