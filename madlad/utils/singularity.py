import subprocess

from madlad.utils import get_pdfset_singularity, get_model_singularity


def create_singularity_build(pdf_id: int, model_name: str, repo: str):
    r"""Create a Singularity build file.

    Args:
        pdf_id (int): LHAPDF ID.
        model_name (str): model name.
    """
    with open("singularity", "w") as f:
        f.write("""Bootstrap: docker
From: """+repo+"""

%post"""+get_pdfset_singularity(pdf_id)+get_model_singularity(model_name))


def build_sif(pdf_id: int, model_name: str, repo: str = "tzuhanchang/madlad:amd64", remote: bool = False):
    r"""Build a Singularity SIF file.

    Args:
        pdf_id (int): LHAPDF ID.
        model_name (str): model name.
    """
    create_singularity_build(pdf_id=pdf_id, model_name=model_name, repo=repo)

    build_option = "--remote" if remote else "--fakeroot"

    build = subprocess.Popen(["singularity", "build", f"{build_option}", "madlad.sif", "singularity"])
    build.wait()
