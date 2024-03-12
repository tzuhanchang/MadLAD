import argparse

from shutil import which
from madlad.container import DockerBuild, SingularityBuild

def argparser():
    parser = argparse.ArgumentParser(description='Run event generation')
    parser.add_argument('-c', '--config', type=str,  required=True, help='Container building settings.')
    return parser.parse_args()


if __name__ == '__main__':
    args = argparser()

    if which("docker"):
        DockerBuild(args.config)
    
    elif which("singularity"):
        SingularityBuild(args.config)

    else:
        raise EnvironmentError("`Docker` and `singularity` not found on your system. \
                               If you think this is a mistake, please report this to https://github.com/tzuhanchang/MadLAD.")