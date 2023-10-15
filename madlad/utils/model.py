import json
import subprocess

from glob import glob
from typing import Optional


def get_model(model_name: str, model_dict: Optional[str] = "/app/MG5_aMC_*/models"):
    r"""Download and install MG5 model defined in process file.

    Args:
        model_name (str): model name.
        model_dict (str, optional): MG5 path. (default: :obj:`str`='/app/MG5_aMC_v2_9_16/models')
    """
    model_dict = glob(model_dict)[0]

    with open("madlad/db/models_db.json", "r") as f:
        lookup_dict = json.load(f)

    link = ""
    for key in list(lookup_dict.keys()):
        if model_name in key or key in model_name:
            link = lookup_dict[key]
            fname = key
        if model_name == key:
            link = lookup_dict[key]
            fname = key

    if link == "":
        raise ValueError("Model not found in the MadGraph database. If you think this is an error, please report to https://github.com/tzuhanchang/MadLAD.git.")

    download = subprocess.Popen(["sudo","wget","-P",model_dict+"/",link])
    download.wait()
    unzip    = subprocess.Popen(["sudo","unzip",model_dict+"/%s.zip"%(fname),"-d",model_dict])
    unzip.wait()

    testcard = open('/tmp/convert.dat','w')
    testcard.write("""convert model %s/%s
"""%(model_dict,fname))
    testcard.close()
    convert = subprocess.Popen(["sudo", "/usr/local/bin/mg5", "/tmp/convert.dat"])
    convert.wait()
    cleanup = subprocess.Popen(["rm", "/tmp/convert.dat"])
    cleanup.wait()


def get_model_singularity(model_name: str, model_dict: str = "/app/MG5_aMC_v2_9_16/models") -> str:
    r"""Download and install MG5 model defined in process file to build singularity image.

    Args:
        model_name (str): model name.
        model_dict (str, optional): MG5 path. (default: :obj:`str`='/app/MG5_aMC_v2_9_16/models')
    """
    with open("madlad/db/models_db.json", "r") as f:
        lookup_dict = json.load(f)

    link = ""
    for key in list(lookup_dict.keys()):
        if model_name in key or key in model_name:
            link = lookup_dict[key]
            fname = key
        if model_name == key:
            link = lookup_dict[key]
            fname = key
        if "MSSM_SLHA2" in model_name or "loop_sm" in model_name or "taudecay_UFO" in model_name or "sm" in model_name:
            return ""

    if link == "":
        raise ValueError("Model not found in the MadGraph database. If you think this is an error, please report to https://github.com/tzuhanchang/MadLAD.git.")
    
    to_write = """
    cd %s
    wget %s
    unzip %s.zip
    cd /tmp
    echo -e "convert model %s/%s" > convert.dat
    /usr/local/bin/mg5 convert.dat
    rm convert.dat
    """%(model_dict, link, fname, model_dict, fname)

    return to_write