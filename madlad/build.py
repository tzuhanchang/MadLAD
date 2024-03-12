import argparse

from shutil import which
from madlad.container import DockerBuild

def argparser():
    parser = argparse.ArgumentParser(description='Run event generation')
    parser.add_argument('-c', '--config', type=str,  required=True, help='Container building settings.')
    return parser.parse_args()


if __name__ == '__main__':
    args = argparser()

    if which("docker"):
        DockerBuild(args.config)