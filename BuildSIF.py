import argparse

from shutil import which

from madlad.utils import config, build_sif

def argparser():
    parser = argparse.ArgumentParser(description='Run event generation')
    parser.add_argument('-c', '--config', type=str,  required=True, 
                        help='Configuration/settings file.')
    return parser.parse_args()


if __name__ == '__main__':
    args = argparser()

    settings = config(args.config)

    if which("singularity") is not None:
        build_sif(settings.run['lhaid'],settings.model['model'])
    else:
        raise RuntimeError("Singularity is not detected on your system.")